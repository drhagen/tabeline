import math

import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.testing import assert_data_frames_equal

from .._types import float_data_types, integer_data_types, numeric_types, whole_data_types


@pytest.mark.parametrize("value", [True, False, "hello", ""])
def test_equal_basic(value):
    df = DataFrame(a=Array(value), b=Array(value))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("dtype_left", numeric_types)
@pytest.mark.parametrize("dtype_right", numeric_types)
def test_equal_numeric(dtype_left, dtype_right):
    df = DataFrame(a=Array[dtype_left](2), b=Array[dtype_right](2))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("number", [2.25, math.nan, math.inf, -math.inf])
@pytest.mark.parametrize("dtype", float_data_types)
def test_equal_float(number, dtype):
    df = DataFrame(a=Array[dtype](number), b=Array[dtype](number))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("dtype", [DataType.Boolean, DataType.String])
def test_null_equal_null_basic(dtype):
    df = DataFrame(a=Array[dtype](None), b=Array[dtype](None))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("dtype", [DataType.Boolean, DataType.String])
def test_null_equal_nothing_basic(dtype):
    df = DataFrame(a=Array[dtype](None), b=Array[DataType.Nothing](None))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("dtype_left", [*numeric_types, DataType.Nothing])
@pytest.mark.parametrize("dtype_right", [*numeric_types, DataType.Nothing])
def test_null_equal_null_numeric(dtype_left, dtype_right):
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
    df = DataFrame(a=Array[dtype](number), b=Array[dtype](None))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=Array(False))
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=Array(True))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    "dtype",
    [*numeric_types, DataType.Boolean, DataType.String, DataType.Nothing],
)
def test_nothing_equal_null(dtype):
    df = DataFrame(a=[None, None], b=Array[dtype](None, None))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=[True, True])
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=[False, False])
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("dtype", numeric_types)
def test_nothing_not_equal_non_null(dtype):
    df = DataFrame(a=[None, None], b=Array[dtype](2, 2))

    actual = df.transmute(c="a == b")
    expected = DataFrame(c=[False, False])
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c="a != b")
    expected = DataFrame(c=[True, True])
    assert_data_frames_equal(actual, expected)
