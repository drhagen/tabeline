import math

import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.exceptions import FunctionArgumentCountError, FunctionArgumentTypeError
from tabeline.testing import assert_data_frames_equal

from .._types import numeric_to_float, numeric_to_integer, numeric_types


def test_pmax():
    df = DataFrame(x=[1.0, 5.0, 3.0], y=[4.0, 2.0, 6.0], z=[2.0, 7.0, 1.0])
    actual = df.transmute(result="pmax(x, y, z)")
    expected = DataFrame(result=[4.0, 7.0, 6.0])
    assert actual == expected


def test_pmax_single_argument():
    df = DataFrame(x=[1.0, 5.0, 3.0, 2.0])
    actual = df.transmute(result="pmax(x)")
    expected = DataFrame(result=[1.0, 5.0, 3.0, 2.0])
    assert actual == expected


def test_pmax_with_nulls():
    df = DataFrame(x=[1.0, None, 3.0, 2.0], y=[4.0, 2.0, None, 6.0])
    actual = df.transmute(z="pmax(x, y)")
    expected = DataFrame(z=[4.0, None, None, 6.0])
    assert actual == expected


def test_pmax_with_integers():
    df = DataFrame(x=[1, 5, 3, 2], y=[4, 2, 3, 6])
    actual = df.transmute(z="pmax(x, y)")
    expected = DataFrame(z=[4, 5, 3, 6])
    assert actual == expected


def test_pmax_with_negative_numbers():
    df = DataFrame(x=[-1.0, -5.0, 3.0, -2.0], y=[-4.0, -2.0, -3.0, 6.0])
    actual = df.transmute(z="pmax(x, y)")
    expected = DataFrame(z=[-1.0, -2.0, 3.0, 6.0])
    assert actual == expected


def test_pmax_with_scalar_and_column():
    df = DataFrame(x=[1.0, 5.0, 3.0, 2.0])
    actual = df.transmute(z="pmax(x, 3.0)")
    expected = DataFrame(z=[3.0, 5.0, 3.0, 3.0])
    assert actual == expected


def test_pmax_grouped():
    df = DataFrame(id=[1, 1, 2, 2], x=[1.0, 5.0, 3.0, 2.0], y=[4.0, 2.0, 3.0, 6.0])
    actual = df.group_by("id").transmute(z="pmax(x, y)")
    expected = DataFrame(id=[1, 1, 2, 2], z=[4.0, 5.0, 3.0, 6.0]).group_by("id")
    assert actual == expected


def test_pmax_with_inf():
    df = DataFrame(x=[1.0, math.inf, -math.inf, 2.0], y=[4.0, 2.0, 3.0, math.inf])
    actual = df.transmute(z="pmax(x, y)")
    expected = DataFrame(z=[4.0, math.inf, 3.0, math.inf])
    assert actual == expected


def test_pmin():
    df = DataFrame(x=[1.0, 5.0, 3.0], y=[4.0, 2.0, 6.0], z=[2.0, 7.0, 1.0])
    actual = df.transmute(result="pmin(x, y, z)")
    expected = DataFrame(result=[1.0, 2.0, 1.0])
    assert actual == expected


def test_pmin_single_argument():
    df = DataFrame(x=[1.0, 5.0, 3.0, 2.0])
    actual = df.transmute(result="pmin(x)")
    expected = DataFrame(result=[1.0, 5.0, 3.0, 2.0])
    assert actual == expected


def test_pmin_with_nulls():
    df = DataFrame(x=[1.0, None, 3.0, 2.0], y=[4.0, 2.0, None, 6.0])
    actual = df.transmute(z="pmin(x, y)")
    expected = DataFrame(z=[1.0, None, None, 2.0])
    assert actual == expected


def test_pmin_with_integers():
    df = DataFrame(x=[1, 5, 3, 2], y=[4, 2, 3, 6])
    actual = df.transmute(z="pmin(x, y)")
    expected = DataFrame(z=[1, 2, 3, 2])
    assert actual == expected


def test_pmin_with_negative_numbers():
    df = DataFrame(x=[-1.0, -5.0, 3.0, -2.0], y=[-4.0, -2.0, -3.0, 6.0])
    actual = df.transmute(z="pmin(x, y)")
    expected = DataFrame(z=[-4.0, -5.0, -3.0, -2.0])
    assert actual == expected


def test_pmin_with_scalar_and_column():
    df = DataFrame(x=[1.0, 5.0, 3.0, 2.0])
    actual = df.transmute(z="pmin(x, 3.0)")
    expected = DataFrame(z=[1.0, 3.0, 3.0, 2.0])
    assert actual == expected


def test_pmin_grouped():
    df = DataFrame(id=[1, 1, 2, 2], x=[1.0, 5.0, 3.0, 2.0], y=[4.0, 2.0, 3.0, 6.0])
    actual = df.group_by("id").transmute(z="pmin(x, y)")
    expected = DataFrame(id=[1, 1, 2, 2], z=[1.0, 2.0, 3.0, 2.0]).group_by("id")
    assert actual == expected


def test_pmin_with_inf():
    df = DataFrame(x=[1.0, math.inf, -math.inf, 2.0], y=[4.0, 2.0, 3.0, math.inf])
    actual = df.transmute(z="pmin(x, y)")
    expected = DataFrame(z=[1.0, 2.0, -math.inf, 2.0])
    assert actual == expected


@pytest.mark.parametrize("function", ["pmax", "pmin"])
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[], y=[]),
        DataFrame(x=[], y=[]).group_by(),
        DataFrame(a=[], x=[], y=[]).group_by("a"),
    ],
)
def test_elementwise_extrema_on_empty_data_frame(function, df):
    actual = df.mutate(z=f"{function}(x, y)")
    expected = df.mutate(z="1.0")
    assert actual == expected


@pytest.mark.parametrize("function", ["pmax", "pmin"])
def test_elementwise_extrema_single_argument_with_expression(function):
    df = DataFrame(x=[1.0, 5.0, 3.0, 2.0])
    actual = df.transmute(result=f"{function}(x * 2)")
    expected = DataFrame(result=[2.0, 10.0, 6.0, 4.0])
    assert actual == expected


@pytest.mark.parametrize("dtype", numeric_types)
def test_pmax_with_positive_literal(dtype):
    df = DataFrame(x=Array[dtype](1, 5, 3))
    actual = df.transmute(result="pmax(x, 3)")
    expected = DataFrame(result=Array[dtype](3, 5, 3))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_integer)
def test_pmax_with_negative_literal(original_dtype, expected_dtype):
    df = DataFrame(x=Array[original_dtype](1, 5, 3))
    actual = df.transmute(result="pmax(x, -3)")
    expected = DataFrame(result=Array[expected_dtype](1, 5, 3))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_float)
def test_pmax_with_decimal_literal(original_dtype, expected_dtype):
    df = DataFrame(x=Array[original_dtype](1, 5, 3))
    actual = df.transmute(result="pmax(x, 2.5)")
    expected = DataFrame(result=Array[expected_dtype](2.5, 5, 3))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("dtype", numeric_types)
def test_pmin_with_positive_literal(dtype):
    df = DataFrame(x=Array[dtype](1, 5, 3))
    actual = df.transmute(result="pmin(x, 3)")
    expected = DataFrame(result=Array[dtype](1, 3, 3))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_integer)
def test_pmin_with_negative_literal(original_dtype, expected_dtype):
    df = DataFrame(x=Array[original_dtype](1, 5, 3))
    actual = df.transmute(result="pmin(x, -3)")
    expected = DataFrame(result=Array[expected_dtype](-3, -3, -3))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_float)
def test_pmin_with_decimal_literal(original_dtype, expected_dtype):
    df = DataFrame(x=Array[original_dtype](1, 5, 3))
    actual = df.transmute(result="pmin(x, 2.5)")
    expected = DataFrame(result=Array[expected_dtype](1, 2.5, 2.5))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("function", ["pmax", "pmin"])
def test_elementwise_extrema_rejects_zero_args(function):
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y=f"{function}()")

    assert exc_info.value == FunctionArgumentCountError(function, 1, 0)


@pytest.mark.parametrize("function", ["pmax", "pmin"])
@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_elementwise_extrema_rejects_non_numeric(function, values, expected_type):
    df = DataFrame(x=values)

    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.mutate(y=f"{function}(x)")

    assert exc_info.value == FunctionArgumentTypeError(
        function, "argument", "numeric type", expected_type
    )
