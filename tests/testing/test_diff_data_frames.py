import pytest

from tabeline import DataFrame
from tabeline.exceptions import DataFramesNotEqualError
from tabeline.testing import (
    ArrayDifference,
    DataFrameDifference,
    assert_data_frames_equal,
    diff_data_frames,
)


@pytest.mark.parametrize(
    "data",
    [
        {"a": [1, 2], "b": [True, False]},
        {"x": ["a", "b"], "y": [1.0, 2.0]},
        {"col": [None, None]},
    ],
)
def test_identical_data_frames(data):
    actual = DataFrame(**data)
    expected = DataFrame(**data)
    differences = diff_data_frames(actual, expected)
    assert differences == []


@pytest.mark.parametrize(
    ("actual", "expected", "difference"),
    [
        (
            DataFrame(a=[1, 2]),
            DataFrame(a=[1, 2, 3]),
            DataFrameDifference.Height(actual_height=2, expected_height=3),
        ),
        (
            DataFrame(a=[1]),
            DataFrame(a=[1], b=[2]),
            DataFrameDifference.Width(actual_width=1, expected_width=2),
        ),
        (
            DataFrame(a=[1, 2]).group_by("a"),
            DataFrame(a=[1, 2]),
            DataFrameDifference.Groups(actual_groups=[["a"]], expected_groups=[]),
        ),
        (
            DataFrame(x=[1, 2]),
            DataFrame(y=[1, 2]),
            DataFrameDifference.ColumnName(index=0, actual_name="x", expected_name="y"),
        ),
        (
            DataFrame(a=[1, 2]),
            DataFrame(a=[1, 3]),
            DataFrameDifference.ColumnValue(
                name="a",
                difference=ArrayDifference.Value(index=1, actual_value=2, expected_value=3),
            ),
        ),
    ],
)
def test_data_frame_differences(actual, expected, difference):
    differences = diff_data_frames(actual, expected)
    assert differences[0] == difference


def test_assert_arrays_equal_raises():
    with pytest.raises(DataFramesNotEqualError):
        assert_data_frames_equal(
            DataFrame(a=[1, 2]),
            DataFrame(a=[1, 2, 3]),
        )
