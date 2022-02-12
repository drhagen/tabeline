import pytest

from tabeline import DataTable


def test_filter():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = table.filter("x == max(x)")
    expected = DataTable(x=[1, 1], y=[3, 4])
    assert actual == expected


def test_grouped_filter():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group("x")
    actual = table.filter("y == max(y)")
    expected = DataTable(x=[0, 1, 1], y=[2, 3, 3]).group("x")
    assert actual == expected


def test_filter_out_all_rows():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = table.filter("x == 2")
    expected = DataTable(x=[], y=[])
    assert actual == expected


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]),
        DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group("x"),
        DataTable(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3]).group("x", "y"),
        DataTable(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3])
        .group("x")
        .group("y"),
    ],
)
def test_filter_true(table):
    actual = table.filter("True")
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]),
        DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group("x"),
        DataTable(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3]).group("x", "y"),
        DataTable(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3])
        .group("x")
        .group("y"),
    ],
)
def test_filter_false(table):
    actual = table.filter("False")
    expected = table.slice0([])
    assert actual == expected


@pytest.mark.parametrize("expression", ["True", "False", "row_index1() == 1"])
@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group(),
        DataTable().group().group(),
    ],
)
def test_filter_empty(expression, table):
    actual = table.filter(expression)
    assert actual == table


@pytest.mark.parametrize(
    ["table", "expected"],
    [
        [DataTable.columnless(height=6), DataTable.columnless(height=3)],
        [DataTable.columnless(height=6).group(), DataTable.columnless(height=3).group()],
        [
            DataTable.columnless(height=6).group().group(),
            DataTable.columnless(height=3).group().group(),
        ],
    ],
)
def test_filter_columnless(table, expected):
    actual = table.filter("row_index0() % 2 == 0")
    assert actual == expected


@pytest.mark.parametrize("expression", ["True", "False", "row_index1() == 1"])
@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[], y=[], z=[]),
        DataTable(x=[], y=[]).group(),
        DataTable(x=[]).group().group(),
        DataTable(x=[], y=[], z=[]).group("x"),
        DataTable(x=[], y=[], z=[]).group("x", "y"),
        DataTable(x=[], y=[], z=[]).group("x").group("y"),
    ],
)
def test_filter_rowless(expression, table):
    actual = table.filter(expression)
    assert actual == table
