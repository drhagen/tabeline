import pytest

from tabeline import DataFrame
from tabeline.testing import assert_data_frames_equal


@pytest.mark.parametrize(
    "expression",
    [
        "-n",
        "+n",
        "~n",
        "abs(n)",
        "sqrt(n)",
        "exp(n)",
        "log(n)",
        "log2(n)",
        "log10(n)",
        "floor(n)",
        "ceil(n)",
        "sin(n)",
        "cos(n)",
        "tan(n)",
        "arcsin(n)",
        "arccos(n)",
        "arctan(n)",
        "is_nan(n)",
        "is_finite(n)",
        "n + a",
        "n - a",
        "n * a",
        "n / a",
        "n // a",
        "n % a",
        "n ** a",
        "a + n",
        "a - n",
        "a * n",
        "a / n",
        "a // n",
        "a % n",
        "a ** n",
        "n + n",
        "n - n",
        "n * n",
        "n / n",
        "n // n",
        "n % n",
        "n ** n",
        "first(n)",
        "last(n)",
        "same(n)",
        "std(n)",
        "var(n)",
        "max(n)",
        "min(n)",
        "sum(n)",
        "mean(n)",
        "median(n)",
        "any(n)",
        "all(n)",
        "pmax(n)",
        "pmax(n, a)",
        "pmax(a, n)",
        "pmax(n, n)",
        "pmin(n)",
        "pmin(n, a)",
        "pmin(a, n)",
        "pmin(n, n)",
        "pow(n, a)",
        "pow(a, n)",
        "pow(n, n)",
    ],
)
@pytest.mark.parametrize("nulls", [[], [None, None]])
def test_nothing_is_preserved(expression, nulls):
    df = DataFrame(n=nulls, a=list(range(len(nulls))))
    actual = df.transmute(x=expression)
    expected = DataFrame(x=nulls)
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    "name",
    [
        "first",
        "last",
        "same",
        "std",
        "var",
        "max",
        "min",
        "sum",
        "mean",
        "median",
        "any",
        "all",
    ],
)
def test_nothing_preserving_reduction_with_summarize(name):
    df = DataFrame(n=[None, None])
    actual = df.group_by().summarize(x=f"{name}(n)")
    expected = DataFrame(x=[None])
    assert_data_frames_equal(actual, expected)
