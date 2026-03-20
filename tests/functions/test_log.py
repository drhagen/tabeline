import math

import pytest

from tabeline import Array, DataFrame
from tabeline.testing import assert_data_frames_equal

from .._types import numeric_to_float

absolute_tolerance = 1e-6


def test_log():
    df = DataFrame(x=[1.0, math.e, 1 / math.e, None])
    actual = df.mutate(x="log(x)")
    expected = DataFrame(x=[0.0, 1.0, -1.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_log2():
    df = DataFrame(x=[1.0, 2.0, 0.5, None])
    actual = df.mutate(x="log2(x)")
    expected = DataFrame(x=[0.0, 1.0, -1.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_log10():
    df = DataFrame(x=[1.0, 10.0, 0.1, None])
    actual = df.mutate(x="log10(x)")
    expected = DataFrame(x=[0.0, 1.0, -1.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_float)
@pytest.mark.parametrize("expression", ["log(x)", "log2(x)", "log10(x)"])
def test_float_result_type(expression, original_dtype, expected_dtype):
    df = DataFrame(x=Array[original_dtype](1, 2, 3))
    actual = df.mutate(y=expression)
    assert actual[:, "y"].data_type == expected_dtype


@pytest.mark.parametrize(
    ("expression", "expected_value"),
    [
        ("log(2)", math.log(2)),
        ("log(-2)", math.nan),
        ("log(2.5)", math.log(2.5)),
        ("log2(2)", 1.0),
        ("log2(-2)", math.nan),
        ("log2(2.5)", math.log2(2.5)),
        ("log10(2)", math.log10(2)),
        ("log10(-2)", math.nan),
        ("log10(2.5)", math.log10(2.5)),
    ],
)
def test_literal(expression, expected_value):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=[expected_value])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)
