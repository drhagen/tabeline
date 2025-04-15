mod array;
mod arrow;
mod concatenate;
mod data_frame;
mod data_type;
mod error;
pub mod expression;
mod function;
mod py_expression;
mod py_function;
mod py_scalar;
mod testing;
mod workarounds;

pub use array::PyArray;
pub use concatenate::{concatenate_columns, concatenate_rows};
pub use data_frame::PyDataFrame;
pub use data_type::DataType;
pub use error::{
    ArraysNotEqualError, ColumnAlreadyExistsError, DataFramesNotEqualError, DuplicateColumnError,
    GroupColumnError, GroupIndexOutOfBoundsError, HasGroupsError, IncompatibleTypeError,
    IndexOutOfBoundsError, NoGroupsError, NonexistentColumnError, RenameExistingError,
    UnmatchedColumnsError, UnmatchedGroupLevelsError, UnmatchedHeightError,
};
pub use py_expression::PyExpression;
use pyo3::prelude::*;

#[pymodule(name = "_tabeline")]
mod extension_module {
    #[pymodule_export]
    use super::{
        concatenate_columns, concatenate_rows, ArraysNotEqualError, ColumnAlreadyExistsError,
        DataFramesNotEqualError, DataType, DuplicateColumnError, GroupColumnError,
        GroupIndexOutOfBoundsError, HasGroupsError, IncompatibleTypeError, IndexOutOfBoundsError,
        NoGroupsError, NonexistentColumnError, PyArray, PyDataFrame, PyExpression,
        RenameExistingError, UnmatchedColumnsError, UnmatchedGroupLevelsError,
        UnmatchedHeightError,
    };

    #[pymodule_export]
    use super::py_function::functions;

    #[pymodule_export]
    use super::testing::{
        assert_py_arrays_equal, assert_py_data_frames_equal, diff_py_arrays, diff_py_data_frames,
        ArrayDifference, DataFrameDifference,
    };
}
