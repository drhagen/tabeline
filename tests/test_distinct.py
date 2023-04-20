import pytest

from tabeline import DataTable


def test_distinct():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = table.distinct("x")
    expected = DataTable(x=[0, 1], y=[1, 3])
    assert actual == expected


def test_distinct_unsorted():
    table = DataTable(x=[1, 1, 0, 0], y=[1, 2, 3, 4])
    actual = table.distinct("x")
    expected = DataTable(x=[1, 0], y=[1, 3])
    assert actual == expected


def test_empty_distinct():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = table.distinct()
    expected = DataTable(x=[0], y=[1])
    assert actual == expected


@pytest.mark.parametrize("distinct_columns", [["z"], ["x", "z"], ["z", "x"]])
def test_distinct_with_grouped_column(distinct_columns):
    table = DataTable(
        x=[0, 0, 0, 1, 1, 1, 1], y=["a", "a", "b", "a", "a", "b", "b"], z=[1, 1, 1, 1, 2, 3, 3]
    ).group("x")
    actual = table.distinct(*distinct_columns)
    expected = DataTable(x=[0, 1, 1, 1], y=["a", "a", "a", "b"], z=[1, 1, 2, 3]).group("x")
    assert actual == expected


@pytest.mark.parametrize("distinct_columns", [["z"], ["y", "z"], ["x", "z"]])
def test_distinct_with_two_grouped_columns(distinct_columns):
    table = DataTable(
        x=[0, 0, 0, 1, 1, 1, 1], y=["a", "a", "b", "a", "a", "b", "b"], z=[1, 1, 1, 1, 2, 3, 3]
    ).group("x", "y")
    actual = table.distinct(*distinct_columns)
    expected = DataTable(x=[0, 0, 1, 1, 1], y=["a", "b", "a", "a", "b"], z=[1, 1, 1, 2, 3]).group(
        "x", "y"
    )
    assert actual == expected


@pytest.mark.parametrize("distinct_columns", [["z"], ["y", "z"], ["x", "z"]])
def test_distinct_with_two_separate_grouped_columns(distinct_columns):
    table = (
        DataTable(
            x=[0, 0, 0, 1, 1, 1, 1], y=["a", "a", "b", "a", "a", "b", "b"], z=[1, 1, 1, 1, 2, 3, 3]
        )
        .group("x")
        .group("y")
    )
    actual = table.distinct(*distinct_columns)
    expected = (
        DataTable(x=[0, 0, 1, 1, 1], y=["a", "b", "a", "a", "b"], z=[1, 1, 1, 2, 3])
        .group("x")
        .group("y")
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
def test_distinct_on_empty(table):
    actual = table.distinct()
    assert actual == table


@pytest.mark.parametrize("columns", [[], ["x"], ["x", "y"], ["y", "x"]])
@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[], y=[], z=[]),
        DataTable(x=[], y=[]).group(),
        DataTable(x=[], y=[]).group().group(),
    ],
)
def test_distinct_on_rowless(columns, table):
    actual = table.distinct(*columns)
    assert actual == table


@pytest.mark.parametrize(
    ["table", "expected"],
    [
        [DataTable.columnless(height=6), DataTable.columnless(height=1)],
        [DataTable.columnless(height=6).group(), DataTable.columnless(height=1).group()],
        [
            DataTable.columnless(height=6).group().group(),
            DataTable.columnless(height=1).group().group(),
        ],
    ],
)
def test_distinct_on_columnless(table, expected):
    actual = table.distinct()
    assert actual == expected
