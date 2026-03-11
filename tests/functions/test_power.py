import math

import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.exceptions import FunctionArgumentCountError, FunctionArgumentTypeError
from tabeline.testing import assert_data_frames_equal

from .._types import float_to_float, integer_to_float, numeric_to_float, whole_to_whole

absolute_tolerance = 1e-6


def test_sqrt():
    df = DataFrame(x=[0.0, 4.0, 6.25, None])
    actual = df.mutate(x="sqrt(x)")
    expected = DataFrame(x=[0.0, 2.0, 2.5, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_exp():
    df = DataFrame(x=[0.0, 1.0, 2.5, None])
    actual = df.mutate(x="exp(x)")
    expected = DataFrame(x=[1.0, math.e, math.exp(2.5), None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_pow():
    df = DataFrame(x=[2.0, 2.0, 4.0, None], y=[2.0, -2.0, 0.5, 3.0])
    actual = df.transmute(z="pow(x, y)")
    expected = DataFrame(z=[4.0, 0.25, 2.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(
    ("original_dtype", "expected_dtype"),
    whole_to_whole + integer_to_float + float_to_float,
)
def test_pow_with_positive_literal_exponent(original_dtype, expected_dtype):
    df = DataFrame(x=Array[original_dtype](2, None))
    actual = df.transmute(result="pow(x, 3)")
    expected = DataFrame(result=Array[expected_dtype](8, None))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_float)
def test_pow_with_negative_literal_exponent(original_dtype, expected_dtype):
    df = DataFrame(x=Array[original_dtype](2, None))
    actual = df.transmute(result="pow(x, -3)")
    expected = DataFrame(result=Array[expected_dtype](0.125, None))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(
    ("original_dtype", "expected_dtype"),
    whole_to_whole + integer_to_float + float_to_float,
)
def test_pow_with_positive_literal_base(original_dtype, expected_dtype):
    df = DataFrame(x=Array[original_dtype](2, None))
    actual = df.transmute(result="pow(3, x)")
    expected = DataFrame(result=Array[expected_dtype](9, None))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_float)
def test_pow_with_negative_literal_base(original_dtype, expected_dtype):
    df = DataFrame(x=Array[original_dtype](2, None))
    actual = df.transmute(result="pow(-3, x)")
    expected = DataFrame(result=Array[expected_dtype](9, None))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_float)
@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("pow(x, 2.5)", [32, None]),
        ("pow(2.5, x)", [39.0625, None]),
    ],
)
def test_pow_with_decimal_literal(original_dtype, expected_dtype, expression, expected):
    df = DataFrame(x=Array[original_dtype](4, None))
    actual = df.transmute(result=expression)
    expected = DataFrame(result=Array[expected_dtype](*expected))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(
    ("expression", "expected_value"),
    [
        ("sqrt(4)", 2.0),
        ("sqrt(-4)", math.nan),
        ("sqrt(6.25)", 2.5),
        ("exp(2)", math.exp(2)),
        ("exp(-2)", math.exp(-2)),
        ("exp(2.5)", math.exp(2.5)),
    ],
)
def test_float_literal(expression, expected_value):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=[expected_value])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_pow_rejects_one_arg():
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="pow(x)")

    assert exc_info.value == FunctionArgumentCountError("pow", 2, 1)


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_pow_rejects_non_numeric_base(values, expected_type):
    df = DataFrame(x=values)

    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.mutate(y="pow(x, 2)")

    assert exc_info.value == FunctionArgumentTypeError(
        "pow", "base", "numeric type", expected_type
    )


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_pow_rejects_non_numeric_exponent(values, expected_type):
    df = DataFrame(x=[1, 2, 3], y=values)

    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.mutate(z="pow(x, y)")

    assert exc_info.value == FunctionArgumentTypeError(
        "pow", "exponent", "numeric type", expected_type
    )
