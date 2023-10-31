import math
import operator

import pytest

from tabeline import DataFrame
from tabeline.testing import assert_data_frame_equal

interesting_numbers = [1, 0, -5, 1.0, 0.0, -0.0, -15.3, math.inf, -math.inf, math.nan]


@pytest.mark.parametrize("left", interesting_numbers)
@pytest.mark.parametrize("right", interesting_numbers)
@pytest.mark.parametrize(
    ("operator", "comparer"),
    [
        ("+", operator.add),
        ("-", operator.sub),
        ("*", operator.mul),
        ("/", operator.truediv),
        ("**", operator.pow),
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
    ("operator", "comparer"),
    [
        ("==", operator.eq),
        ("!=", operator.ne),
        # Polars defines NaNs as the largest floating point values
        (">=", lambda x, y: math.isnan(x) or operator.ge(x, y)),
        ("<=", lambda x, y: math.isnan(y) or operator.le(x, y)),
        (">", lambda x, y: not math.isnan(y) if math.isnan(x) else operator.gt(x, y)),
        ("<", lambda x, y: not math.isnan(x) if math.isnan(y) else operator.lt(x, y)),
    ],
)
def test_comparison_operators(left, right, operator, comparer):
    df = DataFrame(left=[left], right=[right])
    actual = df.transmute(output=f"left {operator} right")
    expected = DataFrame(output=[comparer(left, right)])
    assert actual == expected


@pytest.mark.parametrize("elements", [(1, 2), (1.0, 2.0)])
@pytest.mark.parametrize("operator", ["+", "-", "*", "/", "**", ">=", "<=", ">", "<"])
def test_null_propogation_in_math(elements, operator):
    df = DataFrame(left=[*elements, None, None], right=[elements[0], None, elements[1], None])
    actual = df.transmute(output=f"left {operator} right").slice1([2, 3, 4])
    expected = DataFrame(output=[None, None, None])
    assert actual == expected


@pytest.mark.parametrize("elements", [(True, False), (1, 2), (1.0, 2.0), ("a", "b")])
@pytest.mark.parametrize("operator", ["==", "!="])
def test_null_propogation_in_equality(elements, operator):
    df = DataFrame(left=[*elements, None, None], right=[elements[0], None, elements[1], None])
    actual = df.transmute(output=f"left {operator} right").slice1([2, 3, 4])
    expected = DataFrame(output=[None, None, None])
    assert actual == expected
