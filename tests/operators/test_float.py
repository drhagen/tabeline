import math

import pytest

from tabeline import Array, DataFrame
from tabeline.testing import assert_data_frames_equal

from ._types import float_data_types


@pytest.mark.parametrize("dtype", float_data_types)
@pytest.mark.parametrize("operator", ["+", "-", "*", "/", "//", "%", "**"])
def test_operators_with_nan(dtype, operator):
    df = DataFrame(
        x=Array[dtype](1.0, None, math.inf, -math.inf, math.nan), y=Array[dtype](*[math.nan] * 5)
    )
    expected = DataFrame(z=Array[dtype](math.nan, None, math.nan, math.nan, math.nan))

    actual = df.transmute(z=f"x {operator} y")
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(z=f"y {operator} x")
    assert_data_frames_equal(actual, expected)
