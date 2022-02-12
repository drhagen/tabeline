import pytest

from tabeline import DataTable


def test_unique():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3])
    actual = table.unique()
    expected = DataTable(x=[0, 0, 1], y=[1, 2, 3])
    assert actual == expected


def test_unique_grouped():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group("x")
    actual = table.unique()
    expected = DataTable(x=[0, 0, 1], y=[1, 2, 3]).group("x")
    assert actual == expected


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group(),
        DataTable().group().group(),
    ],
)
def test_unique_empty(table):
    actual = table.unique()
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[], y=[], z=[]),
        DataTable(x=[], y=[]).group(),
        DataTable(x=[], y=[]).group().group(),
    ],
)
def test_unique_rowless(table):
    actual = table.unique()
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable.columnless(height=6),
        DataTable.columnless(height=6).group(),
        DataTable.columnless(height=6).group().group(),
    ],
)
def test_unique_columnless(table):
    actual = table.unique()
    expected = table.slice1([1])
    assert actual == expected
