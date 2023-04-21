import pytest

from tabeline import DataTable


def test_unique():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3])
    actual = table.unique()
    expected = DataTable(x=[0, 0, 1], y=[1, 2, 3])
    assert actual == expected


def test_unique_grouped():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group_by("x")
    actual = table.unique()
    expected = DataTable(x=[0, 0, 1], y=[1, 2, 3]).group_by("x")
    assert actual == expected


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group_by(),
        DataTable().group_by().group_by(),
    ],
)
def test_unique_empty(table):
    actual = table.unique()
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[], y=[], z=[]),
        DataTable(x=[], y=[]).group_by(),
        DataTable(x=[], y=[]).group_by().group_by(),
    ],
)
def test_unique_rowless(table):
    actual = table.unique()
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable.columnless(height=6),
        DataTable.columnless(height=6).group_by(),
        DataTable.columnless(height=6).group_by().group_by(),
    ],
)
def test_unique_columnless(table):
    actual = table.unique()
    expected = table.slice1([1])
    assert actual == expected
