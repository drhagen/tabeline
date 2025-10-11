use crate::array::PyArray;
use crate::arrow::{
    polars_arrow_array_from_pyarrow, record_batches_from_polars_arrow_record_batch,
};
use crate::error::{
    ColumnAlreadyExistsError, DuplicateColumnError, GroupColumnError, HasGroupsError,
    IncompatibleLengthError, IndexOutOfBoundsError, NoGroupsError, NonexistentColumnError,
    RenameExistingError,
};
use crate::expression::Expression;
use crate::py_scalar::PyScalar;
use crate::workarounds::{dummy_column, prepend_dummy_column};
use crate::{GroupIndexOutOfBoundsError, PyExpression};
use polars::error::PolarsError;
use polars::lazy::frame::pivot::pivot_stable;
use polars::prelude::*;
use polars::series::Series;
use polars::{frame::UniqueKeepStrategy, prelude::DataFrame as PolarsDataFrame};
use polars_arrow::array::StructArray;
use pyo3::types::{PyDict, PyTuple};
use pyo3::{prelude::*, IntoPyObjectExt};
use std::collections::{HashMap, HashSet};

pub const DUMMY_NAME: &str = "_dummy";

#[pyclass(frozen, eq, sequence)]
#[derive(Debug, Clone)]
pub struct PyDataFrame {
    pub(crate) polars_data_frame: PolarsDataFrame,
    pub(crate) group_levels: Vec<Vec<String>>,
}

#[pymethods]
impl PyDataFrame {
    #[staticmethod]
    #[pyo3(signature = (columns, /, height))]
    fn from_tuple_list(
        columns: Vec<(String, PyArray)>,
        height: usize,
        py: Python,
    ) -> PyResult<PyDataFrame> {
        // Inject dummy column
        let mut polars_columns = vec![dummy_column(height)];

        // Add user columns
        for (name, array) in columns {
            if array.polars_column.len() != height {
                return Err(PyErr::from_value(
                    IncompatibleLengthError {
                        expected_length: height,
                        actual_length: array.polars_column.len(),
                        column_name: name,
                    }
                    .into_bound_py_any(py)?,
                ));
            }
            polars_columns.push(array.polars_column.with_name(name.into()));
        }

        Ok(PyDataFrame {
            polars_data_frame: PolarsDataFrame::new(polars_columns).unwrap(),
            group_levels: vec![],
        })
    }

    fn to_tuple_list(&self) -> PyResult<Vec<(String, PyArray)>> {
        let mut tuple_list = Vec::new();
        for column in self.polars_data_frame.get_columns() {
            if column.name() == DUMMY_NAME {
                // Skip dummy column
                continue;
            }

            let py_array = PyArray {
                polars_column: column.clone(),
            };
            tuple_list.push((column.name().to_string(), py_array));
        }
        Ok(tuple_list)
    }

    #[getter]
    pub fn height(&self) -> usize {
        self.polars_data_frame.height()
    }

    #[getter]
    pub fn width(&self) -> usize {
        // Subtract 1 for the dummy column
        self.polars_data_frame.width() - 1
    }

    #[getter]
    fn column_names<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyTuple>> {
        let col_names: Vec<&str> = self
            .polars_data_frame
            .get_columns()
            .iter()
            // Skip dummy column
            .filter(|s| s.name() != DUMMY_NAME)
            .map(|s| s.name().as_str())
            .collect();

        PyTuple::new(py, &col_names)
    }

    #[getter]
    fn group_levels<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyTuple>> {
        let mut tuples: Vec<Bound<'py, PyTuple>> = vec![];

        for level in &self.group_levels {
            let tuple = PyTuple::new(py, level.iter().map(|s| s.as_str()))?;
            tuples.push(tuple);
        }

        PyTuple::new(py, tuples)
    }

    #[pyo3(signature = (column_name, /))]
    fn column(&self, column_name: String, py: Python) -> PyResult<PyArray> {
        let col_names = vec![column_name.as_str()];
        self.validate_column_names_exist_vec(&col_names, py)?;

        let series = self.polars_data_frame.column(&column_name).unwrap().clone();

        Ok(PyArray {
            polars_column: series,
        })
    }

    #[pyo3(signature = (index, /))]
    fn row<'py>(&self, index: i64, py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        if index < 0 || index >= self.height() as i64 {
            return Err(PyErr::from_value(
                IndexOutOfBoundsError {
                    index,
                    length: self.height() as i64,
                    one_indexed: false,
                }
                .into_bound_py_any(py)?,
            ));
        }

        let dict = PyDict::new(py);
        for column in self.polars_data_frame.get_columns() {
            if column.name() == DUMMY_NAME {
                // Skip dummy column
                continue;
            }

            dict.set_item(
                column.name().to_string(),
                PyScalar::from(column.get(index as usize).unwrap()).into_bound_py_any(py)?,
            )?;
        }

        Ok(dict)
    }

    #[pyo3(signature = (start, stop, step))]
    fn slice_range0(
        &self,
        start: usize,
        stop: usize,
        step: usize,
        py: Python,
    ) -> PyResult<PyDataFrame> {
        // Implements the slice row operation of __get_item__
        self.validate_no_group_levels(py)?;

        let result = self
            .polars_data_frame
            .clone()
            .lazy()
            .select([all()
                .as_expr()
                .slice(start as i64, (stop - start) as i64)
                .gather_every(step, 0)])
            .collect()
            .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: result,
            group_levels: vec![],
        })
    }

    fn slice0(&self, indexes: Vec<i64>, py: Python) -> PyResult<PyDataFrame> {
        // WORKAROUND: Polars accepts negative indexes with no way to disable
        // this.
        // WORKAROUND: Polars allows slicing a rowless data frame with non-empty
        // indexes.
        // The check that each index is in 1 to height blocks both.
        for &index in &indexes {
            if index < 0 || index >= self.height() as i64 {
                return Err(PyErr::from_value(
                    IndexOutOfBoundsError {
                        index,
                        length: self.height() as i64,
                        one_indexed: false,
                    }
                    .into_bound_py_any(py)?,
                ));
            }
        }

        match self.impl_slice(indexes) {
            Ok(df) => Ok(df),
            Err(e) => match e {
                PolarsError::OutOfBounds(message) => Err(PyErr::from_value(
                    GroupIndexOutOfBoundsError {
                        message: message.to_string(),
                    }
                    .into_bound_py_any(py)?,
                )),
                _ => panic!("{:?}", e),
            },
        }
    }

    #[pyo3(signature = (indexes, /))]
    fn slice1(&self, indexes: Vec<i64>, py: Python) -> PyResult<PyDataFrame> {
        // WORKAROUND: Polars accepts negative indexes with no way to disable
        // this.
        // WORAROUND: Polars allows slicing a rowless data frame with non-empty
        // indexes.
        // The check that each index is in 1 until height blocks both.
        for &index in &indexes {
            if index <= 0 || index > self.height() as i64 {
                return Err(PyErr::from_value(
                    IndexOutOfBoundsError {
                        index,
                        length: self.height() as i64,
                        one_indexed: true,
                    }
                    .into_bound_py_any(py)?,
                ));
            }
        }

        match self.impl_slice(
            indexes
                .iter()
                .map(|&i| i.checked_sub(1).expect("Index underflow"))
                .collect(),
        ) {
            Ok(df) => Ok(df),
            Err(e) => match e {
                PolarsError::OutOfBounds(message) => Err(PyErr::from_value(
                    GroupIndexOutOfBoundsError {
                        message: message.to_string(),
                    }
                    .into_bound_py_any(py)?,
                )),
                _ => panic!("{:?}", e),
            },
        }
    }

    #[pyo3(signature = (predicate, /))]
    fn filter(&self, predicate: &PyExpression) -> PyDataFrame {
        let flattened_groups: Vec<&str> = self.iter_group_names().collect();

        let polars_expression = predicate.expression.to_polars();
        let grouped_expression = polars_expression.over(flattened_groups.as_slice());

        let filtered_df = self
            .polars_data_frame
            .clone()
            .lazy()
            .filter(grouped_expression)
            .collect()
            .unwrap();

        PyDataFrame {
            polars_data_frame: filtered_df,
            group_levels: self.group_levels.clone(),
        }
    }

    #[pyo3(signature = (columns, /))]
    fn distinct(&self, columns: Vec<String>, py: Python) -> PyResult<PyDataFrame> {
        let column_names: Vec<&str> = columns.iter().map(|s| s.as_str()).collect();
        self.validate_column_names_unique(&column_names, py)?;
        self.validate_column_names_exist_vec(&column_names, py)?;

        // Create set of selected columns
        let selected_set: HashSet<&str> = column_names.iter().copied().collect();

        // Get unmentioned group columns
        // unique_stable requires them to be String for some reason
        let unmentioned_groups: Vec<String> = self
            .iter_group_names()
            .filter(|&col| !selected_set.contains(col))
            .map(|s| s.to_string())
            .collect();

        // Combine group columns and selected columns
        let mut columns_to_distinct = unmentioned_groups;
        columns_to_distinct.extend(columns);

        // Get distinct rows
        let distinct_df = self
            .polars_data_frame
            .unique_stable(Some(&columns_to_distinct), UniqueKeepStrategy::First, None)
            .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: distinct_df,
            group_levels: self.group_levels.clone(),
        })
    }

    #[pyo3(signature = ())]
    fn unique(&self) -> PyDataFrame {
        let unique_df = self
            .polars_data_frame
            .unique_stable(None, UniqueKeepStrategy::First, None)
            .unwrap();

        PyDataFrame {
            polars_data_frame: unique_df,
            group_levels: self.group_levels.clone(),
        }
    }

    #[pyo3(signature = (columns, /))]
    fn sort(&self, columns: Vec<String>, py: Python) -> PyResult<PyDataFrame> {
        let column_names: Vec<&str> = columns.iter().map(|s| s.as_str()).collect();
        self.validate_column_names_unique(&column_names, py)?;
        self.validate_column_names_exist_vec(&column_names, py)?;
        self.validate_group_names_not_used(&column_names, py)?;

        let flattened_groups: Vec<&str> = self.iter_group_names().collect();

        let polars_columns = columns.iter().map(col).collect::<Vec<_>>();

        let polars_expression = all()
            .as_expr()
            .sort_by(polars_columns, Default::default())
            .over(flattened_groups.as_slice());

        let sorted_df = self
            .polars_data_frame
            .clone()
            .lazy()
            .select(&[polars_expression])
            .collect()
            .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: sorted_df,
            group_levels: self.group_levels.clone(),
        })
    }

    #[pyo3(signature = (columns, /))]
    fn cluster(&self, columns: Vec<String>, py: Python) -> PyResult<PyDataFrame> {
        let column_names: Vec<&str> = columns.iter().map(|s| s.as_str()).collect();
        self.validate_column_names_unique(&column_names, py)?;
        self.validate_column_names_exist_vec(&column_names, py)?;
        self.validate_group_names_not_used(&column_names, py)?;

        let flattened_groups: Vec<&str> = self.iter_group_names().collect();

        // Combine group columns and selected columns
        let mut window_columns = flattened_groups.clone();
        window_columns.extend(column_names);

        let clustered_df = self
            .polars_data_frame
            .clone()
            .lazy()
            .with_column(arange(0.into(), len(), 1, DataType::Int32).alias("_index"))
            .with_column(col("_index").min().over(window_columns))
            .select(&[all()
                .as_expr()
                .sort_by([col("_index")], Default::default())
                .over(flattened_groups.as_slice())])
            .drop(cols(["_index"]))
            .collect()
            .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: clustered_df,
            group_levels: self.group_levels.clone(),
        })
    }

    #[pyo3(signature = (columns, /))]
    fn select(&self, columns: Vec<String>, py: Python) -> PyResult<PyDataFrame> {
        let column_names: Vec<&str> = columns.iter().map(|s| s.as_str()).collect();
        self.validate_column_names_unique(&column_names, py)?;
        self.validate_column_names_exist_vec(&column_names, py)?;

        // Create sets for lookup
        let select_set: HashSet<&str> = column_names.iter().copied().collect();
        let group_set: HashSet<&str> = self.iter_group_names().collect();

        // Find unmentioned group columns that appear in the original column order
        let unmentioned_groups: Vec<&str> = self
            .iter_column_names()
            .filter(|&col| group_set.contains(col) && !select_set.contains(col))
            .collect();

        // Combine unmentioned groups and selected columns in order
        let mut columns_to_select = vec![];
        columns_to_select.extend(unmentioned_groups);
        columns_to_select.extend(column_names.iter());

        // Keep only the selected columns
        let selected_df = self.polars_data_frame.select(columns_to_select).unwrap();

        Ok(PyDataFrame {
            polars_data_frame: selected_df,
            group_levels: self.group_levels.clone(),
        })
    }

    #[pyo3(signature = (columns, /))]
    fn deselect(&self, columns: Vec<String>, py: Python) -> PyResult<PyDataFrame> {
        let column_names: Vec<&str> = columns.iter().map(|s| s.as_str()).collect();
        self.validate_column_names_unique(&column_names, py)?;
        self.validate_column_names_exist_vec(&column_names, py)?;
        self.validate_group_names_not_used(&column_names, py)?;

        // Drop the selected columns
        let dropped_df = self.polars_data_frame.drop_many(column_names);

        Ok(PyDataFrame {
            polars_data_frame: dropped_df,
            group_levels: self.group_levels.clone(),
        })
    }

    #[pyo3(signature = (columns, /))]
    fn rename(&self, columns: Vec<(String, String)>, py: Python) -> PyResult<PyDataFrame> {
        let from_names: Vec<&str> = columns.iter().map(|(_, c)| c.as_str()).collect();
        self.validate_column_names_unique(&from_names, py)?;
        self.validate_column_names_exist_vec(&from_names, py)?;

        let to_names: Vec<&str> = columns.iter().map(|(c, _)| c.as_str()).collect();
        self.validate_column_names_unique(&to_names, py)?;

        // Do not allow renaming to existing columns
        let mut existing_columns: HashSet<&str> = self
            .iter_column_names()
            .filter(|&name| name != DUMMY_NAME)
            .collect();

        for name in &from_names {
            existing_columns.remove(name);
        }

        for (to_name, from_name) in &columns {
            if existing_columns.contains(to_name.as_str()) {
                return Err(PyErr::from_value(
                    RenameExistingError {
                        old_column: from_name.clone(),
                        new_column: to_name.clone(),
                    }
                    .into_bound_py_any(py)?,
                ));
            }
        }

        let column_mapping: HashMap<&str, &str> = columns
            .iter()
            .map(|(old, new)| (new.as_str(), old.as_str()))
            .collect();

        let renamed_df = self
            .polars_data_frame
            .clone()
            .lazy()
            .rename(from_names, to_names, true)
            .collect()
            .unwrap();

        let renamed_group_levels: Vec<Vec<String>> = self
            .group_levels
            .iter()
            .map(|level| {
                level
                    .iter()
                    .map(|col| {
                        column_mapping
                            .get(col.as_str())
                            .map_or(col.clone(), |&new_name| new_name.to_string())
                    })
                    .collect()
            })
            .collect();

        Ok(PyDataFrame {
            polars_data_frame: renamed_df,
            group_levels: renamed_group_levels,
        })
    }

    #[pyo3(signature = (mutators, /))]
    fn mutate(&self, mutators: Vec<(String, PyExpression)>, py: Python) -> PyResult<PyDataFrame> {
        let mutated_names: Vec<&str> = mutators.iter().map(|(c, _)| c.as_str()).collect();
        self.validate_group_names_not_used(&mutated_names, py)?;

        let flattened_groups: Vec<&str> = self.iter_group_names().collect();

        let mut polars_df = self.polars_data_frame.clone().lazy();

        for (column, expression) in &mutators {
            let polars_expression = expression.expression.to_polars();
            let grouped_expression = polars_expression.over(flattened_groups.as_slice());
            let named_expression = grouped_expression.alias(column);

            polars_df = polars_df.with_column(named_expression);
        }

        let mutated_df = polars_df.collect().unwrap();

        Ok(PyDataFrame {
            polars_data_frame: mutated_df,
            group_levels: self.group_levels.clone(),
        })
    }

    #[pyo3(signature = (mutators, /))]
    fn transmute(
        &self,
        mutators: Vec<(String, PyExpression)>,
        py: Python,
    ) -> PyResult<PyDataFrame> {
        let transmuted_names: Vec<&str> = mutators.iter().map(|(c, _)| c.as_str()).collect();
        self.validate_group_names_not_used(&transmuted_names, py)?;

        let flattened_groups: Vec<&str> = self.iter_group_names().collect();

        let mut polars_df = self.polars_data_frame.clone().lazy();

        for (column, expression) in &mutators {
            let polars_expression = expression.expression.to_polars();
            let grouped_expression = polars_expression.over(flattened_groups.as_slice());
            let named_expression = grouped_expression.alias(column);

            polars_df = polars_df.with_column(named_expression);
        }

        let mut all_columns: Vec<&str> = flattened_groups;
        all_columns.extend(transmuted_names);

        let transmuted_df = polars_df
            .select(all_columns.into_iter().map(col).collect::<Vec<Expr>>())
            .collect()
            .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: transmuted_df,
            group_levels: self.group_levels.clone(),
        })
    }

    #[pyo3(signature = (group_level, /))]
    fn group_by(&self, group_level: Vec<String>, py: Python<'_>) -> PyResult<PyDataFrame> {
        let column_names: Vec<&str> = group_level.iter().map(|s| s.as_str()).collect();
        self.validate_column_names_unique(&column_names, py)?;
        self.validate_column_names_exist_vec(&column_names, py)?;
        self.validate_group_names_not_used(&column_names, py)?;

        // Append the new group level
        let mut new_group_levels = self.group_levels.clone();
        new_group_levels.push(group_level);

        Ok(PyDataFrame {
            polars_data_frame: self.polars_data_frame.clone(),
            group_levels: new_group_levels,
        })
    }

    #[pyo3(signature = ())]
    fn ungroup(&self, py: Python) -> PyResult<PyDataFrame> {
        let new_group_levels = self.drop_one_group_level(py)?;

        Ok(PyDataFrame {
            polars_data_frame: self.polars_data_frame.clone(),
            group_levels: new_group_levels,
        })
    }

    #[pyo3(signature = ())]
    fn ungroup_all(&self) -> PyDataFrame {
        PyDataFrame {
            polars_data_frame: self.polars_data_frame.clone(),
            group_levels: vec![],
        }
    }

    #[pyo3(signature = (columns, /))]
    fn summarize(&self, columns: Vec<(String, PyExpression)>, py: Python) -> PyResult<PyDataFrame> {
        let summarized_names: Vec<&str> = columns.iter().map(|(c, _)| c.as_str()).collect();
        self.validate_group_names_not_used(&summarized_names, py)?;
        let new_group_levels = self.drop_one_group_level(py)?;

        let flattened_groups: Vec<&str> = self.iter_group_names().collect();

        // There is no way to sequentially evaluate expressions in a group_by
        // context, so each reducer must be substituted into subsequent reducers:
        // https://stackoverflow.com/q/71120396/
        let mut substituted_columns = Vec::<(String, Expression)>::new();
        let mut substitutions = HashMap::<&str, Expression>::new();
        for (name, column) in &columns {
            substituted_columns.push((name.clone(), column.expression.substitute(&substitutions)));
            substitutions.insert(name.as_str(), column.expression.clone());
        }

        let mut polars_expressions = vec![];
        for (column, expression) in substituted_columns {
            let polars_expression = expression.to_polars();
            let named_expression = polars_expression.alias(&column);

            polars_expressions.push(named_expression);
        }

        let summarized_df = self
            .polars_data_frame
            .clone()
            .lazy()
            .group_by_stable(flattened_groups)
            .agg(polars_expressions)
            .collect()
            .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: summarized_df,
            group_levels: new_group_levels,
        })
    }

    #[pyo3(signature = (key, value))]
    fn spread(&self, key: String, value: String, py: Python) -> PyResult<PyDataFrame> {
        let produced_column_names = vec![key.as_str(), value.as_str()];
        self.validate_column_names_unique(&produced_column_names, py)?;
        self.validate_column_names_exist_vec(&produced_column_names, py)?;
        self.validate_group_names_not_used(&produced_column_names, py)?;
        let new_group_levels = self.drop_one_group_level(py)?;

        let flattened_groups: Vec<&str> = self.iter_group_names().collect();

        let pivot_df = pivot_stable(
            &self.polars_data_frame,
            &[key],
            Some(flattened_groups),
            Some(&[value]),
            false,
            None,
            None,
        )
        .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: pivot_df,
            group_levels: new_group_levels,
        })
    }

    #[pyo3(signature = (key, value, columns))]
    fn gather(
        &self,
        key: String,
        value: String,
        columns: Vec<String>,
        py: Python,
    ) -> PyResult<PyDataFrame> {
        let consumed_column_names: Vec<&str> = columns.iter().map(|s| s.as_str()).collect();
        self.validate_column_names_unique(&consumed_column_names, py)?;
        self.validate_column_names_exist_vec(&consumed_column_names, py)?;
        self.validate_group_names_not_used(&consumed_column_names, py)?;
        for name in self.iter_column_names() {
            if name == key.as_str() || name == value.as_str() {
                return Err(PyErr::from_value(
                    ColumnAlreadyExistsError {
                        column_name: name.to_string(),
                    }
                    .into_bound_py_any(py)?,
                ));
            }
        }

        let consumed_column_set: HashSet<&str> = consumed_column_names.iter().copied().collect();
        let unpivot_columns: Vec<&str> = self
            .iter_column_names()
            .filter(|&col| !consumed_column_set.contains(col))
            .collect();

        let unpivot_df = self
            .polars_data_frame
            .clone()
            .lazy()
            .unpivot(UnpivotArgsDSL {
                index: cols(unpivot_columns),
                on: cols(consumed_column_names),
                variable_name: Some(key.clone().into()),
                value_name: Some(value.into()),
            })
            .collect()
            .unwrap();

        let mut new_group_levels = self.group_levels.clone();
        new_group_levels.push(vec![key]);

        Ok(PyDataFrame {
            polars_data_frame: unpivot_df,
            group_levels: new_group_levels,
        })
    }

    #[pyo3(signature = (other, by, /))]
    fn inner_join(
        &self,
        other: &PyDataFrame,
        by: Vec<(String, String)>,
        py: Python,
    ) -> PyResult<PyDataFrame> {
        let (left_columns, right_columns) = self.validate_join_by(&by, other, py)?;

        let joined_df = self
            .polars_data_frame
            .clone()
            .join(
                &other.polars_data_frame,
                left_columns,
                right_columns,
                JoinArgs {
                    how: JoinType::Inner,
                    validation: JoinValidation::ManyToMany,
                    suffix: None,
                    slice: None,
                    nulls_equal: true,
                    coalesce: JoinCoalesce::CoalesceColumns,
                    maintain_order: MaintainOrderJoin::LeftRight,
                },
                None,
            )
            .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: joined_df,
            group_levels: vec![],
        })
    }

    #[pyo3(signature = (other, by, /))]
    fn outer_join(
        &self,
        other: &PyDataFrame,
        by: Vec<(String, String)>,
        py: Python,
    ) -> PyResult<PyDataFrame> {
        let (left_columns, right_columns) = self.validate_join_by(&by, other, py)?;

        let joined_df = self
            .polars_data_frame
            .clone()
            .join(
                &other.polars_data_frame,
                left_columns,
                right_columns,
                JoinArgs {
                    how: JoinType::Full,
                    validation: JoinValidation::ManyToMany,
                    suffix: None,
                    slice: None,
                    nulls_equal: true,
                    coalesce: JoinCoalesce::CoalesceColumns,
                    maintain_order: MaintainOrderJoin::LeftRight,
                },
                None,
            )
            .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: joined_df,
            group_levels: vec![],
        })
    }

    #[pyo3(signature = (other, by, /))]
    fn left_join(
        &self,
        other: &PyDataFrame,
        by: Vec<(String, String)>,
        py: Python,
    ) -> PyResult<PyDataFrame> {
        let (left_columns, right_columns) = self.validate_join_by(&by, other, py)?;

        let joined_df = self
            .polars_data_frame
            .clone()
            .join(
                &other.polars_data_frame,
                left_columns,
                right_columns,
                JoinArgs {
                    how: JoinType::Left,
                    validation: JoinValidation::ManyToMany,
                    suffix: None,
                    slice: None,
                    nulls_equal: true,
                    coalesce: JoinCoalesce::CoalesceColumns,
                    maintain_order: MaintainOrderJoin::LeftRight,
                },
                None,
            )
            .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: joined_df,
            group_levels: vec![],
        })
    }

    fn __str__(&self) -> String {
        let levels_str = if !self.group_levels.is_empty() {
            format!(
                "group_levels: {}\n",
                self.group_levels
                    .iter()
                    .map(|level| format!("[{}]", level.join(",")))
                    .collect::<Vec<_>>()
                    .join(", ")
            )
        } else {
            String::new()
        };
        format!(
            "{}{}",
            levels_str,
            self.polars_data_frame
                .clone()
                .lazy()
                .drop(cols([DUMMY_NAME]))
                .collect()
                .unwrap()
        )
    }

    #[staticmethod]
    #[pyo3(signature = (path, /))]
    fn read_csv(path: String) -> PyResult<PyDataFrame> {
        let polars_data_frame = CsvReadOptions::default()
            .with_has_header(true)
            .try_into_reader_with_file_path(Some(path.into()))
            .unwrap()
            .finish()
            .unwrap();

        Ok(PyDataFrame {
            polars_data_frame: prepend_dummy_column(polars_data_frame),
            group_levels: vec![],
        })
    }

    #[pyo3(signature = (path, /))]
    fn write_csv(&self, path: String, py: Python) -> PyResult<()> {
        self.validate_no_group_levels(py)?;

        let buffer = std::fs::File::create(path).unwrap();

        CsvWriter::new(buffer)
            .include_header(true)
            .finish(&mut self.polars_data_frame.drop(DUMMY_NAME).unwrap().clone())
            .unwrap();

        Ok(())
    }

    #[staticmethod]
    #[pyo3(signature = (record_batch, /))]
    fn from_pyarrow_record_batch(record_batch: &Bound<PyAny>) -> PyResult<PyDataFrame> {
        // Get the height from pyarrow because StructArray.len is private for some reason
        let height = record_batch.getattr("num_rows")?.extract::<usize>()?;

        // Import the array
        let polars_arrow_array = polars_arrow_array_from_pyarrow(record_batch)?;

        // Convert to struct array
        let array_struct = polars_arrow_array
            .as_any()
            .downcast_ref::<StructArray>()
            .unwrap();

        // Convert to Columns
        let mut columns = vec![dummy_column(height)];
        for (field, array) in array_struct.fields().iter().zip(array_struct.values()) {
            let series = Series::try_from((field.name.clone(), array.clone())).unwrap();
            columns.push(series.into_column());
        }

        // Convert to DataFrame
        Ok(PyDataFrame {
            polars_data_frame: DataFrame::new(columns).unwrap(),
            group_levels: vec![],
        })
    }

    fn to_pyarrow_record_batches(&self) -> PyResult<Vec<Py<PyAny>>> {
        // Inspired by polars_python::dataframe::PyDataFrame::to_pandas
        Python::attach(|py| {
            let pyarrow = py.import("pyarrow")?;

            let rbs = self
                .polars_data_frame
                .iter_chunks(CompatLevel::oldest(), true)
                .map(|rb| {
                    let pyarrow_record_batch =
                        record_batches_from_polars_arrow_record_batch(&pyarrow, rb)?;

                    Ok(pyarrow_record_batch.unbind())
                })
                .collect::<PyResult<_>>()?;
            Ok(rbs)
        })
    }
}

impl PartialEq for PyDataFrame {
    fn eq(&self, other: &Self) -> bool {
        // WORKAROUND: The dummy column is important here because not all
        // empty polars data frames are equal
        // https://github.com/pola-rs/polars/issues/20555
        self.polars_data_frame
            .equals_missing(&other.polars_data_frame)
            && self.group_levels == other.group_levels
    }
}

impl PyDataFrame {
    pub(crate) fn iter_column_names(&self) -> impl Iterator<Item = &str> {
        // Contains dummy column
        self.polars_data_frame
            .get_columns()
            .iter()
            .map(|s| s.name().as_str())
    }

    pub(crate) fn iter_columns(&self) -> impl Iterator<Item = (&str, PyArray)> {
        // Does not contain dummy column
        self.polars_data_frame
            .get_columns()
            .iter()
            .filter(|s| s.name() != DUMMY_NAME)
            .map(|s| {
                (
                    s.name().as_str(),
                    PyArray {
                        polars_column: s.clone(),
                    },
                )
            })
    }

    fn validate_column_names_unique(&self, column_names: &[&str], py: Python<'_>) -> PyResult<()> {
        let mut seen_columns = HashSet::new();

        for column_name in column_names {
            if !seen_columns.insert(column_name) {
                return Err(PyErr::from_value(
                    DuplicateColumnError {
                        column_name: column_name.to_string(),
                    }
                    .into_bound_py_any(py)?,
                ));
            }
        }

        Ok(())
    }

    fn validate_column_names_exist_vec(
        &self,
        column_names: &[&str],
        py: Python<'_>,
    ) -> PyResult<()> {
        let existing_columns: HashSet<&str> = self.iter_column_names().collect();

        for column_name in column_names {
            match existing_columns.get(column_name) {
                Some(_) => {}
                None => {
                    return Err(PyErr::from_value(
                        NonexistentColumnError {
                            column_name: column_name.to_string(),
                            existing_column_names: existing_columns
                                .iter()
                                .map(|s| s.to_string())
                                .collect(),
                        }
                        .into_bound_py_any(py)?,
                    ));
                }
            }
        }

        Ok(())
    }

    fn validate_group_names_not_used(&self, column_names: &[&str], py: Python<'_>) -> PyResult<()> {
        let group_levels_set: HashSet<&str> = self
            .group_levels
            .iter()
            .flat_map(|level| level.iter())
            .map(|s| s.as_str())
            .collect();

        for column_name in column_names {
            if group_levels_set.contains(column_name) {
                return Err(PyErr::from_value(
                    GroupColumnError {
                        column_name: column_name.to_string(),
                    }
                    .into_bound_py_any(py)?,
                ));
            }
        }

        Ok(())
    }

    fn iter_group_names(&self) -> impl Iterator<Item = &str> {
        // WORKAROUND: Many operations fail if the group columns are empty
        // Always include the dummy column as a group column to ensure that
        // groups are never empty
        std::iter::once(DUMMY_NAME).chain(
            self.group_levels
                .iter()
                .flat_map(|level| level.iter().map(|s| s.as_str())),
        )
    }

    fn drop_one_group_level(&self, py: Python) -> PyResult<Vec<Vec<String>>> {
        if self.group_levels.is_empty() {
            return Err(PyErr::from_value(NoGroupsError {}.into_bound_py_any(py)?));
        } else {
            Ok(self.group_levels[..self.group_levels.len() - 1].to_vec())
        }
    }

    fn impl_slice(&self, indexes: Vec<i64>) -> Result<PyDataFrame, PolarsError> {
        if indexes.is_empty() {
            // WORKAROUND: Polars explodes an empty list into a null instead of
            // no rows. Return no rows instead.
            // https://github.com/pola-rs/polars/issues/6723
            Ok(PyDataFrame {
                polars_data_frame: self.polars_data_frame.head(Some(0)),
                group_levels: self.group_levels.clone(),
            })
        } else {
            // There is no easy way to slice by groups in Polars. Using
            // `gather` on a group causes the sliced columns to be a column of
            // lists that must be exploded at the end. The exploding results
            // in clustering, so getting back the original row order requires
            // tagging each row with an index and sorting the result by that.
            // https://stackoverflow.com/q/71373783/

            let flattened_groups: Vec<&str> = self.iter_group_names().collect();

            // Get non-group columns
            let group_set: HashSet<&str> = flattened_groups.iter().copied().collect();
            let mut non_group_columns: Vec<&str> = self
                .iter_column_names()
                .filter(|&col| !group_set.contains(col))
                .collect();
            non_group_columns.push("_index");

            let result =
                self.polars_data_frame
                    .clone()
                    .lazy()
                    .with_column(arange(0.into(), len(), 1, DataType::Int32).alias("_index"))
                    .group_by_stable(flattened_groups)
                    .agg([all().as_expr().gather(Expr::Literal(LiteralValue::Series(
                        SpecialEq::new(Series::new("".into(), &indexes)),
                    )))])
                    .explode(cols(non_group_columns))
                    .sort(["_index"], Default::default())
                    .drop(cols(["_index"]))
                    .collect();

            match result {
                Ok(polars_data_frame) => Ok(PyDataFrame {
                    polars_data_frame,
                    group_levels: self.group_levels.clone(),
                }),
                Err(e) => Err(e),
            }
        }
    }

    fn validate_no_group_levels(&self, py: Python) -> PyResult<()> {
        if !self.group_levels.is_empty() {
            return Err(PyErr::from_value(
                HasGroupsError {
                    group_levels: self.group_levels.clone(),
                }
                .into_bound_py_any(py)?,
            ));
        }

        Ok(())
    }

    fn validate_join_by<'by>(
        &self,
        by: &'by [(String, String)],
        other: &PyDataFrame,
        py: Python,
    ) -> PyResult<(Vec<&'by str>, Vec<&'by str>)> {
        // Check for duplicate column names in the join keys
        let left_names: Vec<&str> = by.iter().map(|(l, _)| l.as_str()).collect();
        self.validate_column_names_unique(&left_names, py)?;
        self.validate_column_names_exist_vec(&left_names, py)?;

        let right_names: Vec<&str> = by.iter().map(|(_, r)| r.as_str()).collect();
        other.validate_column_names_unique(&right_names, py)?;
        other.validate_column_names_exist_vec(&right_names, py)?;

        // Error on any group levels for now
        // TODO: Implement joining on grouped data frames
        self.validate_no_group_levels(py)?;
        other.validate_no_group_levels(py)?;

        // Prepend the dummy column so that it does not get duplicated
        let mut left_names_with_dummy = vec![DUMMY_NAME];
        left_names_with_dummy.extend(left_names);

        let mut right_names_with_dummy = vec![DUMMY_NAME];
        right_names_with_dummy.extend(right_names);

        Ok((left_names_with_dummy, right_names_with_dummy))
    }
}
