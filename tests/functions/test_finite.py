import math

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
