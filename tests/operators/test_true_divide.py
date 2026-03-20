import math

import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.testing import assert_data_frames_equal

from .._types import (
    float_data_types,
    integer_data_types,
    numeric_to_float,
    whole_data_types,
)

absolute_tolerance = 1e-6


@pytest.mark.parametrize("left_dtype", whole_data_types + integer_data_types)
@pytest.mark.parametrize("right_dtype", whole_data_types + integer_data_types)
@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (1, 2, 0.5),
        (1, 0, math.nan),  # Because there is no +/- integer 0
        (1, None, None),
        (None, 2, None),
        (None, None, None),
    ],
)
def test_true_divide_positive(left_dtype, right_dtype, left, right, answer):
    df = DataFrame(a=Array[left_dtype](left), b=Array[right_dtype](right))
    actual = df.transmute(c="a / b")
    expected = DataFrame(c=Array[DataType.Float64](answer))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize("left_dtype", integer_data_types)
@pytest.mark.parametrize("right_dtype", integer_data_types)
@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (-7, -2, 3.5),
        (-5, 2, -2.5),
        (7, -2, -3.5),
        (0, -4, 0.0),
        (-1, 0, math.nan),  # Because there is no +/- integer 0
    ],
)
def test_true_divide_negative(left_dtype, right_dtype, left, right, answer):
    df = DataFrame(a=Array[left_dtype](left), b=Array[right_dtype](right))
    actual = df.transmute(c="a / b")
    expected = DataFrame(c=Array[DataType.Float64](answer))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (6.25, 2.5, 2.5),
        (1.0, 0.0, math.inf),
        (-1.0, 0.0, -math.inf),
        (1.0, math.inf, 0.0),
        (-1.0, math.inf, -0.0),
        (math.inf, 2.5, math.inf),
        (-math.inf, 2.5, -math.inf),
        (6.25, math.inf, 0.0),
        (math.inf, math.inf, math.nan),
        (math.inf, -math.inf, math.nan),
        (-math.inf, math.inf, math.nan),
    ],
)
@pytest.mark.parametrize("dtype", float_data_types)
def test_true_divide_float(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a / b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_float)
@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("x / 2", [1, None]),
        ("4 / x", [2, None]),
        ("x / -2", [-1, None]),
        ("-4 / x", [-2, None]),
        ("x / 0.5", [4, None]),
        ("4.5 / x", [2.25, None]),
    ],
)
def test_true_divide_with_literal(original_dtype, expected_dtype, expression, expected):
    df = DataFrame(x=Array[original_dtype](2, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[expected_dtype](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)
