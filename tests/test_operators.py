import math
import operator

import pytest

from tabeline import DataFrame
from tabeline.testing import assert_data_frame_equal

interesting_numbers = [1, 0, -5, 1.0, 0.0, -0.0, -15.3, math.inf, -math.inf, math.nan]


@pytest.mark.parametrize("left", interesting_numbers)
@pytest.mark.parametrize("right", interesting_numbers)
@pytest.mark.parametrize(
    ["operator", "comparer"],
    [
        ["+", operator.add],
        ["-", operator.sub],
        ["*", operator.mul],
        ["/", operator.truediv],
        ["**", operator.pow],
    ],
)
def test_numeric_operators(left, right, operator, comparer):
    df = DataFrame(left=[left], right=[right])
    actual = df.transmute(output=f"left {operator} right")

    try:
        output = comparer(left, right)
    except ZeroDivisionError:
        # Skip divide by zero
        return

    if isinstance(output, complex):
        # Python pow returns complex, while we want nan
        output = math.nan

    expected = DataFrame(output=[output])
    assert_data_frame_equal(actual, expected)


@pytest.mark.parametrize("left", interesting_numbers)
@pytest.mark.parametrize("right", interesting_numbers)
@pytest.mark.parametrize(
    ["operator", "comparer"],
    [
        ["==", operator.eq],
        ["!=", operator.ne],
        [">=", operator.ge],
        ["<=", operator.le],
        [">", operator.gt],
        ["<", operator.lt],
    ],
)
def test_comparison_operators(left, right, operator, comparer):
    df = DataFrame(left=[left], right=[right])
    actual = df.transmute(output=f"left {operator} right")
    expected = DataFrame(output=[comparer(left, right)])
    assert actual == expected
