import math

import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.testing import assert_data_frames_equal


def test_abs():
    df = DataFrame(x=[-2.5, 2.5, 0.0, -0.0, math.nan, math.inf, -math.inf, None])
    expected = DataFrame(x=[2.5, 2.5, 0.0, 0.0, math.nan, math.inf, math.inf, None])
    actual = df.mutate(x="abs(x)")
    assert actual == expected


@pytest.mark.parametrize(
    ("expression", "expected_value", "expected_dtype"),
    [
        ("abs(2)", 2, DataType.Whole64),
        ("abs(-3)", 3, DataType.Integer64),
        ("abs(2.5)", 2.5, DataType.Float64),
    ],
)
def test_abs_literal(expression, expected_value, expected_dtype):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=Array[expected_dtype](expected_value))
    assert_data_frames_equal(actual, expected)
