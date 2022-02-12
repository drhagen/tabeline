import pytest

from tabeline import DataTable


def test_sort():
    table = DataTable(x=[1, 0, 2, 1, 1], y=[2.1, 1.0, 0.0, 3.4, 2.1], z=[1, 2, 3, 4, 5])
    actual = table.sort("x")
    expected = DataTable(x=[0, 1, 1, 1, 2], y=[1.0, 2.1, 3.4, 2.1, 0.0], z=[2, 1, 4, 5, 3])
    assert actual == expected


def test_sort_two():
    table = DataTable(x=[1, 0, 2, 1, 1], y=[2.1, 1.0, 0.0, 3.4, 2.1], z=[1, 2, 3, 4, 5])
    actual = table.sort("x", "y")
    expected = DataTable(x=[0, 1, 1, 1, 2], y=[1.0, 2.1, 2.1, 3.4, 0.0], z=[2, 1, 5, 4, 3])
    assert actual == expected


def test_sort_grouped():
    table = DataTable(x=[2, 2, 1, 1, 2, 2], y=[3, 4, 3, 1, 1, 3], z=[5, 4, 3, 2, 1, 0]).group("x")
    actual = table.sort("y")
    expected = DataTable(x=[2, 2, 1, 1, 2, 2], y=[1, 3, 1, 3, 3, 4], z=[1, 5, 2, 3, 0, 4]).group(
        "x"
    )
    assert actual == expected


def test_sort_two_grouped():
    table = DataTable(x=[2, 2, 1, 1, 2, 2], y=[3, 4, 3, 1, 1, 3], z=[5, 4, 3, 2, 1, 0]).group("x")
    actual = table.sort("y", "z")
    expected = DataTable(x=[2, 2, 1, 1, 2, 2], y=[1, 3, 1, 3, 3, 4], z=[1, 0, 2, 3, 5, 4]).group(
        "x"
    )
    assert actual == expected


def test_sort_grouped_two():
    table = DataTable(x=[2, 2, 1, 1, 2, 2], y=[3, 3, 3, 1, 1, 3], z=[5, 4, 3, 2, 1, 0]).group(
        "x", "y"
    )
    actual = table.sort("z")
    expected = DataTable(x=[2, 2, 1, 1, 2, 2], y=[3, 3, 3, 1, 1, 3], z=[0, 4, 3, 2, 1, 5]).group(
        "x", "y"
    )
    assert actual == expected


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group(),
        DataTable().group().group(),
    ],
)
def test_sort_empty(table):
    actual = table.sort()
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable.columnless(height=6),
        DataTable.columnless(height=6).group(),
        DataTable.columnless(height=6).group().group(),
    ],
)
def test_sort_columnless(table):
    actual = table.sort()
    assert actual == table


@pytest.mark.parametrize("columns", [[], ["z"], ["z", "y"], ["y", "z"]])
@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[], y=[], z=[]),
        DataTable(x=[], y=[], z=[]).group(),
        DataTable(x=[], y=[], z=[]).group().group(),
        DataTable(x=[], y=[], z=[]).group("x"),
        DataTable(w=[], x=[], y=[], z=[]).group("w").group("x"),
        DataTable(w=[], x=[], y=[], z=[]).group("x", "w"),
    ],
)
def test_sort_rowless(columns, table):
    actual = table.sort()
    assert actual == table
