import math

import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.testing import assert_data_frames_equal

from ._types import float_data_types, integer_data_types, whole_data_types


@pytest.mark.parametrize("dtype_left", whole_data_types + integer_data_types + float_data_types)
@pytest.mark.parametrize("dtype_right", whole_data_types + integer_data_types + float_data_types)
def test_numbers_equal(dtype_left, dtype_right):
    df = DataFrame(a=Array[dtype_left](2), b=Array[dtype_right](2))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("number", [2.25, math.nan, math.inf, -math.inf])
@pytest.mark.parametrize("dtype", float_data_types)
def test_floats_equal(number, dtype):
    df = DataFrame(a=Array[dtype](number), b=Array[dtype](number))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("value", [True, False, "hello", ""])
def test_values_equal(value):
    df = DataFrame(a=Array(value), b=Array(value))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    "dtype_left",
    whole_data_types
    + integer_data_types
    + float_data_types
    + [DataType.Boolean, DataType.String, DataType.Nothing],
)
@pytest.mark.parametrize(
    "dtype_right",
    whole_data_types
    + integer_data_types
    + float_data_types
    + [DataType.Boolean, DataType.String, DataType.Nothing],
)
def test_null_equal_null(dtype_left, dtype_right):
    if dtype_left == DataType.String or dtype_right == DataType.String:
        pytest.skip("Polars will not compare strings to numbers")

    df = DataFrame(a=Array[dtype_left](None), b=Array[dtype_right](None))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types)
def test_integers_not_equal_null(dtype):
    df = DataFrame(a=Array[dtype](2), b=Array[dtype](None))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("number", [2.25, math.nan, math.inf, -math.inf])
@pytest.mark.parametrize("dtype", float_data_types)
def test_floats_not_equal_null(number, dtype):
    df = DataFrame(a=Array[DataType.Float32](math.nan), b=Array[DataType.Float32](None))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)
