import math

import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import FunctionArgumentCountError, FunctionArgumentTypeError
from tabeline.testing import assert_data_frames_equal

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


def test_pow_rejects_one_arg():
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="pow(x)")

    error = exc_info.value
    assert error.function == "pow"
    assert error.expected == 2
    assert error.actual == 1


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

    assert exc_info.value.function == "pow"
    assert exc_info.value.actual == expected_type
