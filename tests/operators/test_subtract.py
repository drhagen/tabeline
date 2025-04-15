import math

import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.testing import assert_data_frames_equal

from .._xfail import xfail_param
from ._types import float_data_types, integer_data_types, whole_data_types

absolute_tolerance = 1e-6


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (3, 2, 1),
        (0, 0, 0),
        (2, None, None),
        (None, 3, None),
        (None, None, None),
    ],
)
@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types + float_data_types)
def test_subtraction_positive(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a - b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (-1, -3, 2),
        (-3, -1, -2),
        (3, -4, 7),
        (-4, 5, -9),
    ],
)
@pytest.mark.parametrize("dtype", integer_data_types + float_data_types)
def test_subtraction_negative(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a - b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (2.25, 3.75, -1.5),
        (math.inf, 3.25, math.inf),
        (2.25, -math.inf, math.inf),
        (2.25, math.inf, -math.inf),
        (-math.inf, math.inf, -math.inf),
        (math.inf, math.inf, math.nan),
    ],
)
@pytest.mark.parametrize("dtype", float_data_types)
def test_subtraction_float(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a - b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(
    ("left_dtype", "right_dtype", "answer_dtype"),
    [
        xfail_param(DataType.Whole8, DataType.Integer8, DataType.Integer8),
        (DataType.Whole8, DataType.Integer64, DataType.Integer64),
        (DataType.Whole8, DataType.Float32, DataType.Float32),
        (DataType.Whole8, DataType.Float64, DataType.Float64),
        xfail_param(DataType.Whole64, DataType.Integer8, DataType.Integer8),
        xfail_param(DataType.Whole64, DataType.Integer64, DataType.Integer64),
        xfail_param(DataType.Whole64, DataType.Float32, DataType.Float32),
        (DataType.Whole64, DataType.Float64, DataType.Float64),
        (DataType.Integer8, DataType.Float32, DataType.Float32),
        (DataType.Integer8, DataType.Float64, DataType.Float64),
        xfail_param(DataType.Integer64, DataType.Float32, DataType.Float32),
        (DataType.Integer64, DataType.Float64, DataType.Float64),
        (DataType.Float32, DataType.Float64, DataType.Float64),
    ],
)
def test_add_casting(left_dtype, right_dtype, answer_dtype):
    df = DataFrame(a=Array[left_dtype](2), b=Array[right_dtype](4))

    actual = df.transmute(c="a - b")
    expected = DataFrame(c=Array[answer_dtype](-2))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)

    actual = df.transmute(c="b - a")
    expected = DataFrame(c=Array[answer_dtype](2))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types + float_data_types)
@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("x - 1", [3, None]),
        ("4 - x", [0, None]),
    ],
)
def test_subtract_with_constant_integer(dtype, expression, expected):
    df = DataFrame(x=Array[dtype](4, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[dtype](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize("dtype", float_data_types)
@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("x - 1.5", [2.5, None]),
        ("3.75 - x", [-0.25, None]),
    ],
)
def test_subtract_float_with_constant_decimal(dtype, expression, expected):
    df = DataFrame(x=Array[dtype](4, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[dtype](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types)
@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("x - 1.5", [2.5, None]),
        ("3.75 - x", [-0.25, None]),
    ],
)
def test_subtract_integer_with_constant_decimal(dtype, expression, expected):
    df = DataFrame(x=Array[dtype](4, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[DataType.Float64](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)
