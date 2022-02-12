import pytest

from tabeline import DataTable


def test_cluster():
    table = DataTable(x=[1, 0, 1, 0], y=[3, 1, 2, 4])
    actual = table.cluster("x")
    expected = DataTable(x=[1, 1, 0, 0], y=[3, 2, 1, 4])
    assert actual == expected


def test_cluster_two():
    table = DataTable(x=[2, 2, 1, 1, 2, 2], y=[3, 4, 4, 3, 4, 3], z=[1, 2, 3, 4, 5, 6])
    actual = table.cluster("x", "y")
    expected = DataTable(x=[2, 2, 2, 2, 1, 1], y=[3, 3, 4, 4, 4, 3], z=[1, 6, 2, 5, 3, 4])
    assert actual == expected


def test_cluster_grouped():
    table = DataTable(x=[2, 2, 1, 1, 2, 2], y=[3, 4, 4, 3, 4, 3], z=[1, 2, 3, 4, 5, 6]).group("x")
    actual = table.cluster("y")
    expected = DataTable(x=[2, 2, 1, 1, 2, 2], y=[3, 3, 4, 3, 4, 4], z=[1, 6, 3, 4, 2, 5]).group(
        "x"
    )
    assert actual == expected


def test_cluster_grouped_two():
    table = DataTable(
        x=[2, 2, 1, 1, 2, 2, 2], y=[3, 4, 4, 4, 4, 3, 4], z=[2, 1, 1, 1, 2, 1, 1]
    ).group("x", "y")
    actual = table.cluster("z")
    expected = DataTable(
        x=[2, 2, 1, 1, 2, 2, 2], y=[3, 4, 4, 4, 4, 3, 4], z=[2, 1, 1, 1, 1, 1, 2]
    ).group("x", "y")
    assert actual == expected


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group(),
        DataTable().group().group(),
    ],
)
def test_cluster_empty(table):
    actual = table.cluster()
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable.columnless(height=6),
        DataTable.columnless(height=6).group(),
        DataTable.columnless(height=6).group().group(),
    ],
)
def test_cluster_columnless(table):
    actual = table.cluster()
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
def test_cluster_rowless(columns, table):
    actual = table.cluster()
    assert actual == table
