import math

import pytest

from tabeline import DataFrame
from tabeline.testing import assert_data_frame_equal

from ._xfail import xfail_param

zero_argument_functions = [
    "n",
    "row_index0",
    "row_index1",
]

one_argument_functions = [
    "abs",
    "sqrt",
    "log",
    "log2",
    "log10",
    "exp",
    "sin",
    "cos",
    "tan",
    "arcsin",
    "arccos",
    "arctan",
    "floor",
    "ceil",
    "is_nan",
    "std",
    "var",
    "max",
    "min",
    "sum",
    "mean",
    "median",
    "any",
    "all",
    "first",
    "last",
]


@pytest.mark.parametrize(
    ["name", "function"],
    [
        ["abs", abs],
        ["sqrt", math.sqrt],
        ["log", math.log],
        ["log2", math.log2],
        ["log10", math.log10],
        ["exp", math.exp],
        ["sin", math.sin],
        ["cos", math.cos],
        ["tan", math.tan],
        ["arcsin", math.asin],
        ["arccos", math.acos],
        ["arctan", math.atan],
        ["floor", math.floor],
        ["ceil", math.ceil],
    ],
)
def test_single_numeric_argument_against_python(name, function):
    values = [0.5, 1.0, math.pi / 4]
    df = DataFrame(x=values)
    actual = df.transmute(y=f"{name}(x)")
    expected = DataFrame(y=[function(value) for value in values])
    assert_data_frame_equal(actual, expected, reltol=1e-8)


@pytest.mark.parametrize("name", zero_argument_functions)
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
        DataFrame(a=[]).group_by("a"),
        DataFrame(a=[], b=[]).group_by("a", "b"),
        DataFrame(a=[], b=[]).group_by("a").group_by("b"),
    ],
)
def test_zero_argument_functions_on_rowless_data_frame_with_mutate(name, df):
    actual = df.mutate(x=f"{name}()")
    expected = df.mutate(x="1")
    assert actual == expected


@pytest.mark.parametrize("name", zero_argument_functions)
@pytest.mark.parametrize(
    "df",
    [
        # Polars chokes on empty list in groupby
        # https://github.com/pola-rs/polars/issues/3041
        xfail_param(DataFrame()),
        xfail_param(DataFrame().group_by()),
        xfail_param(DataFrame().group_by().group_by()),
        xfail_param(DataFrame(a=[])),
        DataFrame(a=[]).group_by("a"),
        DataFrame(a=[], b=[]).group_by("a", "b"),
        DataFrame(a=[], b=[]).group_by("a").group_by("b"),
    ],
)
def test_zero_argument_functions_on_rowless_data_frame_with_summarize(name, df):
    expected = df.mutate(x="1")

    actual = df.group_by().summarize(x=f"{name}()")
    assert actual == expected


# Skip any and all because Polars has no concept of List[Nothing]. This will
# probably have to be handled by separate dtypes stored in Tabeline.
@pytest.mark.parametrize(
    "name", [xfail_param(f) if f in ("all", "any") else f for f in one_argument_functions]
)
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(a=[]),
        DataFrame(a=[]).group_by(),
        DataFrame(a=[]).group_by().group_by(),
        DataFrame(a=[]).group_by("a"),
        DataFrame(a=[], b=[], c=[]).group_by("a", "b"),
        DataFrame(a=[], b=[], c=[]).group_by("a").group_by("b"),
    ],
)
def test_one_argument_functions_on_rowless_data_frame_with_mutate(name, df):
    actual = df.mutate(x=f"{name}(a)")
    expected = df.mutate(x="1")
    assert actual == expected


def test_quantile():
    actual = DataFrame(x=[20, 21, 22]).mutate(q="quantile(x, 0.75)")
    expected = DataFrame(x=[20, 21, 22], q=[21.5, 21.5, 21.5])
    assert_data_frame_equal(actual, expected, reltol=1e-8)


def test_trapz():
    df = DataFrame(id=[0, 0, 0, 1, 1, 1], t=[2, 4, 5, 10, 11, 14], y=[0, 1, 1, 2, 3, 4])
    actual = df.group_by("id").summarize(q="trapz(t, y)")
    expected = DataFrame(id=[0, 1], q=[2.0, 13.0])
    assert_data_frame_equal(actual, expected, reltol=1e-8)
