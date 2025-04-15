import math

from tabeline import DataFrame


def test_abs():
    df = DataFrame(x=[-2.5, 2.5, 0.0, -0.0, math.nan, math.inf, -math.inf, None])
    expected = DataFrame(x=[2.5, 2.5, 0.0, 0.0, math.nan, math.inf, math.inf, None])
    actual = df.mutate(x="abs(x)")
    assert actual == expected
