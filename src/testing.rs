use std::fmt::Display;

use pyo3::{prelude::*, IntoPyObjectExt};

use crate::{
    error::{ArraysNotEqualError, DataFramesNotEqualError},
    py_scalar::PyScalar,
    DataType, PyArray, PyDataFrame,
};

#[pyclass(frozen, eq, str)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ArrayDifference {
    Count {
        actual_count: usize,
        expected_count: usize,
    },
    Type {
        actual_type: DataType,
        expected_type: DataType,
    },
    Value {
        index: usize,
        actual_value: PyScalar,
        expected_value: PyScalar,
    },
}

impl Display for ArrayDifference {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ArrayDifference::Count {
                actual_count,
                expected_count,
            } => write!(
                f,
                "Expected {} elements, but found {} elements",
                expected_count, actual_count
            ),
            ArrayDifference::Type {
                actual_type,
                expected_type,
            } => write!(
                f,
                "Expected elements of type {}, but found elements of type {}",
                expected_type, actual_type
            ),
            ArrayDifference::Value {
                index,
                actual_value,
                expected_value,
            } => write!(
                f,
                "At index {}, expected value {}, but found value {}",
                index, expected_value, actual_value
            ),
        }
    }
}

#[pymethods]
impl ArrayDifference {
    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }
}

#[pyclass(frozen, eq, str)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DataFrameDifference {
    Height {
        actual_height: usize,
        expected_height: usize,
    },
    Width {
        actual_width: usize,
        expected_width: usize,
    },
    Groups {
        actual_groups: Vec<Vec<String>>,
        expected_groups: Vec<Vec<String>>,
    },
    ColumnName {
        index: usize,
        actual_name: String,
        expected_name: String,
    },
    ColumnValue {
        name: String,
        difference: ArrayDifference,
    },
}

impl Display for DataFrameDifference {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DataFrameDifference::Height {
                actual_height,
                expected_height,
            } => write!(
                f,
                "Expected height of {}, but found height of {}",
                expected_height, actual_height
            ),
            DataFrameDifference::Width {
                actual_width,
                expected_width,
            } => write!(
                f,
                "Expected width of {}, but found width of {}",
                expected_width, actual_width
            ),
            DataFrameDifference::Groups {
                actual_groups,
                expected_groups,
            } => write!(
                f,
                "Expected groups {}, but found groups {}",
                expected_groups
                    .iter()
                    .map(|group| format!("[{}]", group.join(", ")))
                    .collect::<Vec<_>>()
                    .join(", "),
                actual_groups
                    .iter()
                    .map(|group| format!("[{}]", group.join(", ")))
                    .collect::<Vec<_>>()
                    .join(", ")
            ),
            DataFrameDifference::ColumnName {
                index,
                actual_name,
                expected_name,
            } => write!(
                f,
                "At index {}, expected column name {}, but found column name {}",
                index, expected_name, actual_name
            ),
            DataFrameDifference::ColumnValue { name, difference } => {
                write!(f, "In column {}: {}", name, difference)
            }
        }
    }
}

#[pymethods]
impl DataFrameDifference {
    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }
}
#[pyfunction]
#[pyo3(signature = (actual, expected, /, *, relative_tolerance = 0.0, absolute_tolerance = 0.0))]
pub fn diff_py_arrays(
    actual: &PyArray,
    expected: &PyArray,
    relative_tolerance: f64,
    absolute_tolerance: f64,
) -> Vec<ArrayDifference> {
    let mut differences = Vec::new();

    if actual.len() != expected.len() {
        differences.push(ArrayDifference::Count {
            actual_count: actual.len(),
            expected_count: expected.len(),
        });
    }

    if actual.data_type() != expected.data_type() {
        differences.push(ArrayDifference::Type {
            actual_type: actual.data_type(),
            expected_type: expected.data_type(),
        });
    }

    if !differences.is_empty() {
        // Return early if the counts or types are different
        return differences;
    }

    match actual.data_type() {
        DataType::Float32 => {
            for (i, (actual_value, expected_value)) in actual
                .polars_column
                .f32()
                .unwrap()
                .into_iter()
                .zip(expected.polars_column.f32().unwrap().into_iter())
                .enumerate()
            {
                match (actual_value, expected_value) {
                    (Some(actual_value), Some(expected_value)) => {
                        let absolute_difference = (actual_value - expected_value).abs();
                        if absolute_difference > absolute_tolerance as f32 {
                            let relative_difference = absolute_difference / expected_value.abs();
                            if relative_difference > relative_tolerance as f32 {
                                differences.push(ArrayDifference::Value {
                                    index: i,
                                    actual_value: PyScalar::Float(actual_value as f64),
                                    expected_value: PyScalar::Float(expected_value as f64),
                                });
                            }
                        }
                    }
                    (Some(actual_value), None) => {
                        differences.push(ArrayDifference::Value {
                            index: i,
                            actual_value: PyScalar::Float(actual_value as f64),
                            expected_value: PyScalar::Null,
                        });
                    }
                    (None, Some(expected_value)) => {
                        differences.push(ArrayDifference::Value {
                            index: i,
                            actual_value: PyScalar::Null,
                            expected_value: PyScalar::Float(expected_value as f64),
                        });
                    }
                    (None, None) => {}
                }
            }
        }
        DataType::Float64 => {
            for (i, (actual_value, expected_value)) in actual
                .polars_column
                .f64()
                .unwrap()
                .into_iter()
                .zip(expected.polars_column.f64().unwrap().into_iter())
                .enumerate()
            {
                match (actual_value, expected_value) {
                    (Some(actual_value), Some(expected_value)) => {
                        let absolute_difference = (actual_value - expected_value).abs();
                        if absolute_difference > absolute_tolerance {
                            let relative_difference = absolute_difference / expected_value.abs();
                            if relative_difference > relative_tolerance {
                                differences.push(ArrayDifference::Value {
                                    index: i,
                                    actual_value: PyScalar::Float(actual_value),
                                    expected_value: PyScalar::Float(expected_value),
                                });
                            }
                        }
                    }
                    (Some(actual_value), None) => {
                        differences.push(ArrayDifference::Value {
                            index: i,
                            actual_value: PyScalar::Float(actual_value),
                            expected_value: PyScalar::Null,
                        });
                    }
                    (None, Some(expected_value)) => {
                        differences.push(ArrayDifference::Value {
                            index: i,
                            actual_value: PyScalar::Null,
                            expected_value: PyScalar::Float(expected_value),
                        });
                    }
                    (None, None) => {}
                }
            }
        }
        _ => {
            for (i, (actual_value, expected_value)) in actual
                .polars_column
                .clone()
                .into_materialized_series()
                .iter()
                .zip(
                    expected
                        .polars_column
                        .clone()
                        .into_materialized_series()
                        .iter(),
                )
                .enumerate()
            {
                if actual_value != expected_value {
                    differences.push(ArrayDifference::Value {
                        index: i,
                        actual_value: PyScalar::from(actual_value),
                        expected_value: PyScalar::from(expected_value),
                    });
                }
            }
        }
    }

    differences
}

#[pyfunction]
#[pyo3(signature = (actual, expected, /, *, relative_tolerance = 0.0, absolute_tolerance = 0.0))]
pub fn diff_py_data_frames(
    actual: &PyDataFrame,
    expected: &PyDataFrame,
    relative_tolerance: f64,
    absolute_tolerance: f64,
) -> Vec<DataFrameDifference> {
    let mut differences = Vec::new();

    if actual.height() != expected.height() {
        differences.push(DataFrameDifference::Height {
            actual_height: actual.height(),
            expected_height: expected.height(),
        });
    }

    if actual.width() != expected.width() {
        differences.push(DataFrameDifference::Width {
            actual_width: actual.width(),
            expected_width: expected.width(),
        });
    }

    if actual.group_levels != expected.group_levels {
        differences.push(DataFrameDifference::Groups {
            actual_groups: actual.group_levels.clone(),
            expected_groups: expected.group_levels.clone(),
        });
    }

    if !differences.is_empty() {
        // Return early if the shapes or groups are different
        return differences;
    }

    for (i, ((actual_name, actual_array), (expected_name, expected_array))) in actual
        .iter_columns()
        .zip(expected.iter_columns())
        .enumerate()
    {
        if actual_name != expected_name {
            differences.push(DataFrameDifference::ColumnName {
                index: i,
                actual_name: actual_name.to_owned(),
                expected_name: expected_name.to_owned(),
            });
        }

        if let Some(difference) = diff_py_arrays(
            &actual_array,
            &expected_array,
            relative_tolerance,
            absolute_tolerance,
        )
        .first()
        {
            differences.push(DataFrameDifference::ColumnValue {
                name: actual_name.to_owned(),
                difference: difference.clone(),
            });
        }
    }

    differences
}

#[pyfunction]
#[pyo3(signature = (actual, expected, /, *, relative_tolerance = 0.0, absolute_tolerance = 0.0))]
pub fn assert_py_data_frames_equal(
    actual: &PyDataFrame,
    expected: &PyDataFrame,
    relative_tolerance: f64,
    absolute_tolerance: f64,
    py: Python,
) -> PyResult<()> {
    let differences = diff_py_data_frames(actual, expected, relative_tolerance, absolute_tolerance);
    if !differences.is_empty() {
        return Err(PyErr::from_value(
            DataFramesNotEqualError { differences }.into_bound_py_any(py)?,
        ));
    } else {
        Ok(())
    }
}

#[pyfunction]
#[pyo3(signature = (actual, expected, /, *, relative_tolerance = 0.0, absolute_tolerance = 0.0))]
pub fn assert_py_arrays_equal(
    actual: &PyArray,
    expected: &PyArray,
    relative_tolerance: f64,
    absolute_tolerance: f64,
    py: Python,
) -> PyResult<()> {
    let differences: Vec<ArrayDifference> =
        diff_py_arrays(actual, expected, relative_tolerance, absolute_tolerance);
    if !differences.is_empty() {
        return Err(PyErr::from_value(
            ArraysNotEqualError { differences }.into_bound_py_any(py)?,
        ));
    } else {
        Ok(())
    }
}
