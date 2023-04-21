import pytest

from tabeline import DataTable


def test_filter():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = table.filter("x == max(x)")
    expected = DataTable(x=[1, 1], y=[3, 4])
    assert actual == expected


def test_grouped_filter():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group_by("x")
    actual = table.filter("y == max(y)")
    expected = DataTable(x=[0, 1, 1], y=[2, 3, 3]).group_by("x")
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
        DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group_by("x"),
        DataTable(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3]).group_by("x", "y"),
        DataTable(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3])
        .group_by("x")
        .group_by("y"),
    ],
)
def test_filter_true(table):
    actual = table.filter("True")
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]),
        DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group_by("x"),
        DataTable(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3]).group_by("x", "y"),
        DataTable(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3])
        .group_by("x")
        .group_by("y"),
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
        DataTable().group_by(),
        DataTable().group_by().group_by(),
    ],
)
def test_filter_empty(expression, table):
    actual = table.filter(expression)
    assert actual == table


@pytest.mark.parametrize(
    ["table", "expected"],
    [
        [DataTable.columnless(height=6), DataTable.columnless(height=3)],
        [DataTable.columnless(height=6).group_by(), DataTable.columnless(height=3).group_by()],
        [
            DataTable.columnless(height=6).group_by().group_by(),
            DataTable.columnless(height=3).group_by().group_by(),
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
        DataTable(x=[], y=[]).group_by(),
        DataTable(x=[]).group_by().group_by(),
        DataTable(x=[], y=[], z=[]).group_by("x"),
        DataTable(x=[], y=[], z=[]).group_by("x", "y"),
        DataTable(x=[], y=[], z=[]).group_by("x").group_by("y"),
    ],
)
def test_filter_rowless(expression, table):
    actual = table.filter(expression)
    assert actual == table
