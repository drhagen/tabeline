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
        (2, 3, 8),
        (3, 2, 9),
        (0, 2, 0),
        (2, 0, 1),
        (0, 0, 1),  # Only because Python does this
        (2, None, None),
        (None, 3, None),
        (None, None, None),
    ],
)
@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types + float_data_types)
def test_power_positive(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a ** b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("left", "left_dtype", "right", "right_dtype", "answer", "answer_dtype"),
    [
        # Negative base with whole exponent
        (-2, DataType.Integer8, 2, DataType.Whole8, 4, DataType.Integer8),
        (-2, DataType.Integer8, 3, DataType.Whole64, -8, DataType.Integer8),
        (-2, DataType.Integer64, 2, DataType.Whole8, 4, DataType.Integer64),
        (-2, DataType.Integer64, 3, DataType.Whole64, -8, DataType.Integer64),
        (-2, DataType.Float32, 2, DataType.Whole8, 4, DataType.Float32),
        (-2, DataType.Float32, 3, DataType.Whole64, -8, DataType.Float32),
        (-2, DataType.Float64, 2, DataType.Whole8, 4, DataType.Float64),
        (-2, DataType.Float64, 3, DataType.Whole64, -8, DataType.Float64),
        # Positive base with negative integer exponent
        # Polars will not treat anything ** signed as float
        # https://github.com/pola-rs/polars/issues/15897
        xfail_param(2, DataType.Whole8, -2, DataType.Integer8, 0.25, DataType.Float64),
        xfail_param(2, DataType.Whole8, 2, DataType.Integer64, 4, DataType.Float64),
        xfail_param(2, DataType.Whole64, -2, DataType.Integer8, 0.25, DataType.Float64),
        xfail_param(2, DataType.Whole64, 2, DataType.Integer64, 4, DataType.Float64),
        xfail_param(2, DataType.Integer8, -2, DataType.Integer8, 0.25, DataType.Float64),
        xfail_param(2, DataType.Integer8, 2, DataType.Integer64, 4, DataType.Float64),
        xfail_param(2, DataType.Integer64, -2, DataType.Integer8, 0.25, DataType.Float64),
        xfail_param(2, DataType.Integer64, 2, DataType.Integer64, 4, DataType.Float64),
        (2, DataType.Float32, -2, DataType.Integer8, 0.25, DataType.Float32),
        (2, DataType.Float32, 2, DataType.Integer64, 4, DataType.Float32),
        (2, DataType.Float64, -2, DataType.Integer8, 0.25, DataType.Float64),
        (2, DataType.Float64, 2, DataType.Integer64, 4, DataType.Float64),
    ],
)
def test_power_integer(left, left_dtype, right, right_dtype, answer, answer_dtype):
    df = DataFrame(a=Array[left_dtype](left), b=Array[right_dtype](right))
    actual = df.transmute(c="a ** b")
    expected = DataFrame(c=Array[answer_dtype](answer))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (2.5, 2.0, 6.25),
        (math.inf, 2.0, math.inf),
        (2.0, math.inf, math.inf),
        (0.5, math.inf, 0.0),
        (2.0, -math.inf, 0.0),
        (0.5, -math.inf, math.inf),
    ],
)
@pytest.mark.parametrize("dtype", float_data_types)
def test_power_float(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a ** b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


# https://github.com/pola-rs/polars/issues/21596
@pytest.mark.skip(
    reason="Polars does not consistently handle the type of literals to the base of pow"
)
@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types + float_data_types)
@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("x ** 3", [8, None]),
        ("3 ** x", [9, None]),
    ],
)
def test_operators_with_constant_integer(dtype, expr, expected):
    df = DataFrame(x=Array[dtype](2, None))
    actual = df.transmute(result=expr)
    expected = DataFrame(result=Array[dtype](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


# https://github.com/pola-rs/polars/issues/21596
@pytest.mark.skip(
    reason="Polars does not consistently handle the type of literals to the base of pow"
)
@pytest.mark.parametrize("dtype", float_data_types)
@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("x ** -3.0", [0.125, None]),
        ("-1.5 ** x", [-2.25, None]),
    ],
)
def test_power_float_with_constant_decimal(dtype, expr, expected):
    df = DataFrame(x=Array[dtype](2, None))
    actual = df.transmute(result=expr)
    expected = DataFrame(result=Array[dtype](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types)
@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("x ** -3.0", [0.125, None]),
        ("-1.5 ** x", [-2.25, None]),
    ],
)
def test_power_integer_with_constant_decimal(dtype, expr, expected):
    df = DataFrame(x=Array[dtype](2, None))
    actual = df.transmute(result=expr)
    expected = DataFrame(result=Array[DataType.Float64](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)
