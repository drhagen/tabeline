import math

import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.testing import assert_data_frames_equal

from .._types import (
    float_data_types,
    integer_data_types,
    numeric_to_float,
    numeric_to_integer,
    numeric_types,
    whole_data_types,
)

absolute_tolerance = 1e-6


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (6, 2, 3),
        (4, 3, 1),
        (0, 3, 0),
        (2, 3, 0),
        (2, None, None),
        (None, 3, None),
        (None, None, None),
    ],
)
@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types + float_data_types)
def test_floor_divide_positive(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a // b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (-7, -2, 3),
        (-4, 3, -2),
        (7, -2, -4),
        (0, -4, 0),
        (-7, -8, 0),
        (-7, 8, -1),
    ],
)
@pytest.mark.parametrize("dtype", integer_data_types + float_data_types)
def test_floor_divide_negative(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a // b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types)
def test_floor_divide_by_zero_integer(dtype):
    df = DataFrame(a=Array[dtype](1, None), b=Array[dtype](0, 0))
    actual = df.transmute(c="a // b")
    expected = DataFrame(c=Array[dtype](None, None))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (9.2, 3.1, 2.0),
        (-3.5, 2.25, -2),
        (7.1, -7.8, -1),
        (-7.1, -7.8, 0),
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
def test_floor_divide_float(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a // b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(
    ("left_dtype", "right_dtype", "answer_dtype"),
    [
        (DataType.Whole8, DataType.Integer8, DataType.Integer8),
        (DataType.Whole8, DataType.Integer64, DataType.Integer64),
        (DataType.Whole8, DataType.Float32, DataType.Float32),
        (DataType.Whole8, DataType.Float64, DataType.Float64),
        (DataType.Whole64, DataType.Integer8, DataType.Integer64),
        (DataType.Whole64, DataType.Integer64, DataType.Integer64),
        (DataType.Whole64, DataType.Float32, DataType.Float32),
        (DataType.Whole64, DataType.Float64, DataType.Float64),
        (DataType.Integer8, DataType.Float32, DataType.Float32),
        (DataType.Integer8, DataType.Float64, DataType.Float64),
        (DataType.Integer64, DataType.Float32, DataType.Float32),
        (DataType.Integer64, DataType.Float64, DataType.Float64),
        (DataType.Float32, DataType.Float64, DataType.Float64),
    ],
)
def test_floor_divide_casting(left_dtype, right_dtype, answer_dtype):
    df = DataFrame(a=Array[left_dtype](9), b=Array[right_dtype](-2))

    actual = df.transmute(c="a // b")
    expected = DataFrame(c=Array[answer_dtype](-5))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)

    actual = df.transmute(c="b // a")
    expected = DataFrame(c=Array[answer_dtype](-1))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize("dtype", numeric_types)
@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("x // 2", [3, None]),
        ("15 // x", [2, None]),
    ],
)
def test_floor_divide_with_positive_literal(dtype, expression, expected):
    df = DataFrame(x=Array[dtype](7, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[dtype](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_integer)
@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("x // -2", [-2, None]),
        ("-7 // x", [-3, None]),
    ],
)
def test_floor_divide_with_negative_literal(original_dtype, expected_dtype, expression, expected):
    df = DataFrame(x=Array[original_dtype](3, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[expected_dtype](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_float)
@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("x // -2.5", [-1, None]),
        ("-6.5 // x", [-4, None]),
    ],
)
def test_floor_divide_with_decimal_literal(original_dtype, expected_dtype, expression, expected):
    df = DataFrame(x=Array[original_dtype](2, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[expected_dtype](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)
