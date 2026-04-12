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
        (2, 3, 5),
        (0, 0, 0),
        (2, None, None),
        (None, 3, None),
        (None, None, None),
    ],
)
@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types + float_data_types)
def test_add_positive(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a + b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (-1, -3, -4),
        (3, -4, -1),
        (-4, 5, 1),
    ],
)
@pytest.mark.parametrize("dtype", integer_data_types + float_data_types)
def test_add_negative(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a + b")
    expected = DataFrame(c=Array[dtype](answer))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        (2.25, 3.25, 5.5),
        (math.inf, 3.25, math.inf),
        (2.25, -math.inf, -math.inf),
        (math.inf, math.inf, math.inf),
        (math.inf, -math.inf, math.nan),
    ],
)
@pytest.mark.parametrize("dtype", float_data_types)
def test_add_float(left, right, answer, dtype):
    df = DataFrame(a=Array[dtype](left), b=Array[dtype](right))
    actual = df.transmute(c="a + b")
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
def test_add_casting(left_dtype, right_dtype, answer_dtype):
    df = DataFrame(a=Array[left_dtype](2), b=Array[right_dtype](-4))
    expected = DataFrame(c=Array[answer_dtype](-2))

    actual = df.transmute(c="a + b")
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)

    actual = df.transmute(c="b + a")
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize("dtype", numeric_types)
@pytest.mark.parametrize("expression", ["x + 2", "2 + x"])
def test_add_with_positive_literal(dtype, expression):
    df = DataFrame(x=Array[dtype](2, 4, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[dtype](4, 6, None))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_integer)
@pytest.mark.parametrize("expression", ["x + -2", "-2 + x"])
def test_add_with_negative_literal(original_dtype, expected_dtype, expression):
    df = DataFrame(x=Array[original_dtype](2, 4, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[expected_dtype](0, 2, None))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_float)
@pytest.mark.parametrize("expression", ["x + 2.5", "2.5 + x"])
def test_add_with_decimal_literal(original_dtype, expected_dtype, expression):
    df = DataFrame(x=Array[original_dtype](2, 4, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[expected_dtype](4.5, 6.5, None))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(
    ("left", "right", "answer"),
    [
        ("a", "b", "ab"),
        ("", "x", "x"),
        ("x", "", "x"),
        ("x", None, None),
        (None, "x", None),
        (None, None, None),
    ],
)
def test_concatenate_strings(left, right, answer):
    df = DataFrame(a=Array[DataType.String](left), b=Array[DataType.String](right))
    actual = df.transmute(c="a + b")
    expected = DataFrame(c=Array[DataType.String](answer))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("value", "answer"),
    [
        ("hello", "hello world"),
        ("", " world"),
        (None, None),
    ],
)
def test_concatenate_column_with_literal(value, answer):
    df = DataFrame(a=Array[DataType.String](value))
    actual = df.transmute(c="a + ' world'")
    expected = DataFrame(c=Array[DataType.String](answer))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("value", "answer"),
    [
        ("world", "hello world"),
        ("", "hello "),
        (None, None),
    ],
)
def test_concatenate_literal_with_column(value, answer):
    df = DataFrame(a=Array[DataType.String](value))
    actual = df.transmute(c="'hello ' + a")
    expected = DataFrame(c=Array[DataType.String](answer))
    assert_data_frames_equal(actual, expected)
