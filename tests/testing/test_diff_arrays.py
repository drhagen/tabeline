import math

import pytest

from tabeline import Array, DataType
from tabeline.exceptions import ArraysNotEqualError
from tabeline.testing import ArrayDifference, assert_arrays_equal, diff_arrays


@pytest.mark.parametrize(
    "values",
    [
        [True, False, None],
        [-1, 2, None],
        [1.0, 2.0, 0.0, -0.0, math.inf, -math.inf, math.nan, None],
        ["a", "b", None],
        [None, None, None],
    ],
)
def test_identical_arrays(values):
    actual = Array(*values)
    expected = Array(*values)
    differences = diff_arrays(actual, expected)
    assert differences == []


@pytest.mark.parametrize(
    ("actual", "expected", "difference"),
    [
        (
            [1, 2],
            [1, 2, 3],
            ArrayDifference.Count(actual_count=2, expected_count=3),
        ),
        (
            [1.0],
            ["a"],
            ArrayDifference.Type(actual_type=DataType.Float64, expected_type=DataType.String),
        ),
        (
            [True, False, True],
            [True, False, False],
            ArrayDifference.Value(index=2, actual_value=True, expected_value=False),
        ),
        (
            [True, False, False],
            [True, None, False],
            ArrayDifference.Value(index=1, actual_value=False, expected_value=None),
        ),
        (
            [1, 2, 3],
            [1, 5, 3],
            ArrayDifference.Value(index=1, actual_value=2, expected_value=5),
        ),
        (
            [1, 2, 3],
            [1, None, 3],
            ArrayDifference.Value(index=1, actual_value=2, expected_value=None),
        ),
        (
            ["a", "b", "c"],
            ["a", "b", "d"],
            ArrayDifference.Value(index=2, actual_value="c", expected_value="d"),
        ),
        (
            ["a", "b", "c"],
            [None, "b", "c"],
            ArrayDifference.Value(index=0, actual_value="a", expected_value=None),
        ),
        (
            [None, 1.0],
            [2.0, 1.0],
            ArrayDifference.Value(index=0, actual_value=None, expected_value=2.0),
        ),
    ],
)
def test_array_differences(actual, expected, difference):
    actual_array = Array(*actual)
    expected_array = Array(*expected)
    differences = diff_arrays(actual_array, expected_array)
    assert differences[0] == difference


@pytest.mark.parametrize(
    (
        "actual_value",
        "expected_value",
        "relative_tolerance",
        "absolute_tolerance",
        "should_differ",
    ),
    [
        (1.0, 1.0, 0.0, 0.0, False),
        (1.0, 2.0, 0.0, 0.0, True),
        (100.0, 101.0, 0.1, 0.0, False),
        (100.0, 99.0, 0.1, 0.0, False),
        (100.0, 101.0, 0.001, 0.0, True),
        (100.0, 99.0, 0.001, 0.0, True),
        (0.0, 0.01, 0.0, 0.1, False),
        (0.0, -0.01, 0.0, 0.1, False),
        (0.0, 0.01, 0.0, 0.001, True),
        (0.0, -0.01, 0.0, 0.001, True),
    ],
)
def test_float_tolerance(
    actual_value, expected_value, relative_tolerance, absolute_tolerance, should_differ
):
    array1 = Array(actual_value)
    array2 = Array(expected_value)
    differences = diff_arrays(
        array1,
        array2,
        relative_tolerance=relative_tolerance,
        absolute_tolerance=absolute_tolerance,
    )
    assert (len(differences) > 0) == should_differ


@pytest.mark.parametrize(
    ("actual", "expected", "differences"),
    [
        (
            ["a", "b"],
            [1, 2, None],
            [
                ArrayDifference.Count(actual_count=2, expected_count=3),
                ArrayDifference.Type(
                    actual_type=DataType.String, expected_type=DataType.Integer64
                ),
            ],
        ),
        (
            [True, False, False, None],
            [True, True, False, False],
            [
                ArrayDifference.Value(index=1, actual_value=False, expected_value=True),
                ArrayDifference.Value(index=3, actual_value=None, expected_value=False),
            ],
        ),
    ],
)
def test_multiple_array_differences(actual, expected, differences):
    actual_array = Array(*actual)
    expected_array = Array(*expected)
    result = diff_arrays(actual_array, expected_array)
    assert result == differences


def test_assert_arrays_equal_raises():
    with pytest.raises(ArraysNotEqualError):
        assert_arrays_equal(Array(1, 2), Array(1, 3))
