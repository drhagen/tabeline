import math

import pytest

from tabeline import Array, DataFrame
from tabeline.testing import assert_data_frames_equal

from .._types import numeric_to_float

absolute_tolerance = 1e-6


def test_sin():
    df = DataFrame(x=[0.0, 1.0, -math.pi, None])
    actual = df.mutate(x="sin(x)")
    expected = DataFrame(x=[0.0, math.sin(1.0), 0.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_cos():
    df = DataFrame(x=[0.0, 1.0, -math.pi, None])
    actual = df.mutate(x="cos(x)")
    expected = DataFrame(x=[1.0, math.cos(1.0), -1.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_tan():
    df = DataFrame(x=[0.0, 1.0, -math.pi, None])
    actual = df.mutate(x="tan(x)")
    expected = DataFrame(x=[0.0, math.tan(1.0), 0.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_arcsin():
    df = DataFrame(x=[0.0, 0.5, -1.0, None])
    actual = df.mutate(x="arcsin(x)")
    expected = DataFrame(x=[0.0, math.asin(0.5), -math.pi / 2, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_arccos():
    df = DataFrame(x=[1.0, 0.5, -1.0, None])
    actual = df.mutate(x="arccos(x)")
    expected = DataFrame(x=[0.0, math.acos(0.5), math.pi, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_arctan():
    df = DataFrame(x=[0.0, 1.0, -1.0, None])
    actual = df.mutate(x="arctan(x)")
    expected = DataFrame(x=[0.0, math.atan(1.0), -math.pi / 4, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


@pytest.mark.parametrize(("original_dtype", "expected_dtype"), numeric_to_float)
@pytest.mark.parametrize(
    "expression",
    ["sin(x)", "cos(x)", "tan(x)", "arcsin(x)", "arccos(x)", "arctan(x)"],
)
def test_float_result_type(expression, original_dtype, expected_dtype):
    df = DataFrame(x=Array[original_dtype](0, None))
    actual = df.mutate(y=expression)
    assert actual[:, "y"].data_type == expected_dtype


@pytest.mark.parametrize(
    ("expression", "expected_value"),
    [
        ("sin(2)", math.sin(2)),
        ("sin(-2)", math.sin(-2)),
        ("sin(2.5)", math.sin(2.5)),
        ("cos(2)", math.cos(2)),
        ("cos(-2)", math.cos(-2)),
        ("cos(2.5)", math.cos(2.5)),
        ("tan(2)", math.tan(2)),
        ("tan(-2)", math.tan(-2)),
        ("tan(2.5)", math.tan(2.5)),
        ("arcsin(1)", math.asin(1)),
        ("arcsin(-1)", math.asin(-1)),
        ("arcsin(0.5)", math.asin(0.5)),
        ("arccos(1)", math.acos(1)),
        ("arccos(-1)", math.acos(-1)),
        ("arccos(0.5)", math.acos(0.5)),
        ("arctan(2)", math.atan(2)),
        ("arctan(-2)", math.atan(-2)),
        ("arctan(2.5)", math.atan(2.5)),
    ],
)
def test_literal(expression, expected_value):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=[expected_value])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)
