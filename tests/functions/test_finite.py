import math

import pytest

from tabeline import DataFrame


def test_is_null():
    df = DataFrame(x=[1.0, math.nan, 2.0, None])
    actual = df.mutate(x="is_null(x)")
    expected = DataFrame(x=[False, False, False, True])
    assert actual == expected


def test_is_nan():
    df = DataFrame(x=[1.0, math.nan, 2.0, None])
    actual = df.mutate(x="is_nan(x)")
    expected = DataFrame(x=[False, True, False, None])
    assert actual == expected


def test_is_finite():
    df = DataFrame(x=[1.0, math.inf, -math.inf, math.nan, None])
    actual = df.mutate(x="is_finite(x)")
    expected = DataFrame(x=[True, False, False, False, None])
    assert actual == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("is_null(2)", False),
        ("is_null(-2)", False),
        ("is_null(2.5)", False),
        ("is_null(nan)", False),
        ("is_null(inf)", False),
        ("is_null(-inf)", False),
    ],
)
def test_is_null_literal(expression, expected):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=[expected])
    assert actual == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("is_nan(2)", False),
        ("is_nan(-2)", False),
        ("is_nan(2.5)", False),
        ("is_nan(nan)", True),
        ("is_nan(inf)", False),
        ("is_nan(-inf)", False),
    ],
)
def test_is_nan_literal(expression, expected):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=[expected])
    assert actual == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("is_finite(2)", True),
        ("is_finite(-2)", True),
        ("is_finite(2.5)", True),
        ("is_finite(nan)", False),
        ("is_finite(inf)", False),
        ("is_finite(-inf)", False),
    ],
)
def test_is_finite_literal(expression, expected):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=[expected])
    assert actual == expected
