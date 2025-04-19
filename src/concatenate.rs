use crate::data_frame::{PyDataFrame, DUMMY_NAME};
use crate::error::{
    DuplicateColumnError, HasGroupsError, UnmatchedColumnsError, UnmatchedGroupLevelsError,
    UnmatchedHeightError,
};
use polars::functions::concat_df_horizontal;
use polars::prelude::*;
use pyo3::{prelude::*, IntoPyObjectExt};
use std::collections::HashSet;

#[pyfunction]
/// Concatenates multiple DataFrames vertically (adding rows)
pub fn concatenate_rows(
    df: &PyDataFrame,
    others: Vec<PyDataFrame>,
    py: Python,
) -> PyResult<PyDataFrame> {
    let mut validated_lazy_frames = vec![df.polars_data_frame.clone().lazy()];
    for other in &others {
        if other.iter_column_names().ne(df.iter_column_names()) {
            return Err(PyErr::from_value(
                UnmatchedColumnsError {
                    expected_columns: df.iter_column_names().map(|c| c.to_string()).collect(),
                    actual_columns: other.iter_column_names().map(|c| c.to_string()).collect(),
                }
                .into_bound_py_any(py)?,
            ));
        }

        if other.group_levels != df.group_levels {
            return Err(PyErr::from_value(
                UnmatchedGroupLevelsError {
                    expected_group_levels: df.group_levels.clone(),
                    actual_group_levels: other.group_levels.clone(),
                }
                .into_bound_py_any(py)?,
            ));
        }

        validated_lazy_frames.push(other.polars_data_frame.clone().lazy());
    }

    // Perform vertical concatenation
    let concatenated = concat(
        validated_lazy_frames,
        UnionArgs {
            parallel: true,
            rechunk: true,
            ..Default::default()
        },
    )
    .unwrap()
    .collect()
    .unwrap();

    Ok(PyDataFrame {
        polars_data_frame: concatenated,
        group_levels: df.group_levels.clone(),
    })
}

#[pyfunction]
/// Concatenates multiple DataFrames horizontally (adding columns)
pub fn concatenate_columns(
    df: &PyDataFrame,
    others: Vec<PyDataFrame>,
    py: Python,
) -> PyResult<PyDataFrame> {
    // Check if first DataFrame has groups
    if !df.group_levels.is_empty() {
        return Err(PyErr::from_value(
            HasGroupsError {
                group_levels: df.group_levels.clone(),
            }
            .into_bound_py_any(py)?,
        ));
    }

    let mut dfs = vec![df.polars_data_frame.clone()];
    let mut found_columns: HashSet<&str> = df.iter_column_names().collect();
    for other in &others {
        if other.height() != df.height() {
            return Err(PyErr::from_value(
                UnmatchedHeightError {
                    expected_height: df.height(),
                    actual_height: other.height(),
                }
                .into_bound_py_any(py)?,
            ));
        }

        if !other.group_levels.is_empty() {
            return Err(PyErr::from_value(
                HasGroupsError {
                    group_levels: other.group_levels.clone(),
                }
                .into_bound_py_any(py)?,
            ));
        }

        // Check for duplicate columns
        for column in other.iter_column_names() {
            if column == DUMMY_NAME {
                continue;
            }

            if found_columns.contains(column) {
                return Err(PyErr::from_value(
                    DuplicateColumnError {
                        column_name: column.to_string(),
                    }
                    .into_bound_py_any(py)?,
                ));
            }
            found_columns.insert(column);
        }

        dfs.push(other.polars_data_frame.clone().drop(DUMMY_NAME).unwrap());
    }

    // Perform horizontal concatenation
    let concatenated = concat_df_horizontal(&dfs, false)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

    Ok(PyDataFrame {
        polars_data_frame: concatenated,
        group_levels: vec![],
    })
}
