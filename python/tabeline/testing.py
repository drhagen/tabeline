__all__ = ["assert_arrays_equal", "assert_data_frames_equal", "diff_arrays", "diff_data_frames"]

from ._array import Array
from ._data_frame import DataFrame
from ._tabeline import (
    ArrayDifference,
    DataFrameDifference,
    assert_py_arrays_equal,
    assert_py_data_frames_equal,
    diff_py_arrays,
    diff_py_data_frames,
)


def diff_arrays(
    actual: Array,
    expected: Array,
    *,
    relative_tolerance: float = 0.0,
    absolute_tolerance: float = 0.0,
) -> ArrayDifference:
    return diff_py_arrays(
        actual._py_array,
        expected._py_array,
        relative_tolerance=relative_tolerance,
        absolute_tolerance=absolute_tolerance,
    )


def diff_data_frames(
    actual: DataFrame,
    expected: DataFrame,
    *,
    relative_tolerance: float = 0.0,
    absolute_tolerance: float = 0.0,
) -> DataFrameDifference:
    return diff_py_data_frames(
        actual._py_data_frame,
        expected._py_data_frame,
        relative_tolerance=relative_tolerance,
        absolute_tolerance=absolute_tolerance,
    )


def assert_arrays_equal(
    actual: Array,
    expected: Array,
    *,
    relative_tolerance: float = 0.0,
    absolute_tolerance: float = 0.0,
) -> None:
    assert_py_arrays_equal(
        actual._py_array,
        expected._py_array,
        relative_tolerance=relative_tolerance,
        absolute_tolerance=absolute_tolerance,
    )


def assert_data_frames_equal(
    actual: DataFrame,
    expected: DataFrame,
    *,
    relative_tolerance: float = 0.0,
    absolute_tolerance: float = 0.0,
) -> None:
    assert_py_data_frames_equal(
        actual._py_data_frame,
        expected._py_data_frame,
        relative_tolerance=relative_tolerance,
        absolute_tolerance=absolute_tolerance,
    )
