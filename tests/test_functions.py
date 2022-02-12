import math

import pytest

from tabeline import DataTable
from tabeline.testing import assert_table_equal

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
        ["floor", math.floor],
        ["ceil", math.ceil],
    ],
)
def test_single_numeric_argument_against_python(name, function):
    values = [0.5, 1.0, math.pi]
    table = DataTable(x=values)
    actual = table.transmute(y=f"{name}(x)")
    expected = DataTable(y=[function(value) for value in values])
    assert_table_equal(actual, expected, reltol=1e-8)


@pytest.mark.parametrize("name", zero_argument_functions)
@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group(),
        DataTable().group().group(),
        DataTable(a=[]).group("a"),
        DataTable(a=[], b=[]).group("a", "b"),
        DataTable(a=[], b=[]).group("a").group("b"),
    ],
)
def test_zero_argument_functions_on_rowless_table_with_mutate(name, table):
    actual = table.mutate(x=f"{name}()")
    expected = table.mutate(x="1")
    assert actual == expected


@pytest.mark.parametrize("name", zero_argument_functions)
@pytest.mark.parametrize(
    "table",
    [
        # Polars chokes on empty list in groupby
        # https://github.com/pola-rs/polars/issues/3041
        xfail_param(DataTable()),
        xfail_param(DataTable().group()),
        xfail_param(DataTable().group().group()),
        xfail_param(DataTable(a=[])),
        DataTable(a=[]).group("a"),
        DataTable(a=[], b=[]).group("a", "b"),
        DataTable(a=[], b=[]).group("a").group("b"),
    ],
)
def test_zero_argument_functions_on_rowless_table_with_summarize(name, table):
    expected = table.mutate(x="1")

    actual = table.group().summarize(x=f"{name}()")
    assert actual == expected


# Skip any and all because Polars has no concept of List[Nothing]. This will
# probably have to be handled by separate dtypes stored in Tabeline.
@pytest.mark.parametrize(
    "name", [xfail_param(f) if f in ("all", "any") else f for f in one_argument_functions]
)
@pytest.mark.parametrize(
    "table",
    [
        DataTable(a=[]),
        DataTable(a=[]).group(),
        DataTable(a=[]).group().group(),
        DataTable(a=[]).group("a"),
        DataTable(a=[], b=[], c=[]).group("a", "b"),
        DataTable(a=[], b=[], c=[]).group("a").group("b"),
    ],
)
def test_one_argument_functions_on_rowless_table_with_mutate(name, table):
    actual = table.mutate(x=f"{name}(a)")
    expected = table.mutate(x="1")
    assert actual == expected


def test_quantile():
    actual = DataTable(x=[20, 21, 22]).mutate(q="quantile(x, 0.75)")
    expected = DataTable(x=[20, 21, 22], q=[21.5, 21.5, 21.5])
    assert_table_equal(actual, expected, reltol=1e-8)


def test_trapz():
    table = DataTable(id=[0, 0, 0, 1, 1, 1], t=[2, 4, 5, 10, 11, 14], y=[0, 1, 1, 2, 3, 4])
    actual = table.group("id").summarize(q="trapz(t, y)")
    expected = DataTable(id=[0, 1], q=[2.0, 13.0])
    assert_table_equal(actual, expected, reltol=1e-8)
