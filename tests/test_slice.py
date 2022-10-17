import pytest

from tabeline import DataTable
from tabeline.exceptions import IndexOutOfRange


def test_slice():
    table = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])

    expected = DataTable(x=[1, 3], y=[True, True], z=[3.5, 6.7])

    actual = table.slice0([0, 2])
    assert actual == expected

    actual = table.slice1([1, 3])
    assert actual == expected


def test_slice_out_of_bounds():
    table = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])

    # General Exception because who know what will come out of Polars
    with pytest.raises(Exception):
        _ = table.slice0([2, 4])

    with pytest.raises(Exception):
        _ = table.slice1([0, 2])


def test_slice_groups():
    table = DataTable(x=[1, 2, 2, 1, 2, 1], y=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5]).group_by("x")

    expected = DataTable(x=[2, 1, 2, 1], y=[6.7, 8.9, -1.1, 4.5]).group_by("x")

    actual = table.slice0([1, 2])
    assert actual == expected

    actual = table.slice1([2, 3])
    assert actual == expected


def test_slice_one_index():
    table = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])

    expected = DataTable(x=[1], y=[True], z=[3.5])

    actual = table.slice0([0])
    assert actual == expected

    actual = table.slice1([1])
    assert actual == expected


def test_slice_groups_one_index():
    table = DataTable(x=[1, 2, 2, 1, 2, 1], y=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5]).group_by("x")

    expected = DataTable(x=[2, 1], y=[6.7, 8.9]).group_by("x")

    actual = table.slice0([1])
    assert actual == expected

    actual = table.slice1([2])
    assert actual == expected


def test_slice_groups_multiple_columns_one_index():
    table = (
        DataTable(
            x=[1, 2, 2, 1, 2, 1, 1, 2],
            y=["a", "a", "a", "a", "b", "b", "b", "b"],
            z=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5, 4.3, 7.7],
        )
        .group_by("x")
        .group_by("y")
    )

    expected = (
        DataTable(x=[2, 1, 1, 2], y=["a", "a", "b", "b"], z=[6.7, 8.9, 4.3, 7.7])
        .group_by("x")
        .group_by("y")
    )

    actual = table.slice0([1])
    assert actual == expected

    actual = table.slice1([2])
    assert actual == expected


def test_slice_to_nothing():
    table = DataTable(x=[1, 2, 2, 1, 2, 1], y=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5])

    expected = DataTable(x=[], y=[])

    actual = table.slice0([])
    assert actual == expected

    actual = table.slice1([])
    assert actual == expected


def test_slice_groups_to_nothing():
    table = DataTable(x=[1, 2, 2, 1, 2, 1], y=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5]).group_by("x")

    expected = DataTable(x=[], y=[]).group_by("x")

    actual = table.slice0([])
    assert actual == expected

    actual = table.slice1([])
    assert actual == expected


def test_slice_multiple_groups_to_nothing():
    table = (
        DataTable(
            x=[1, 2, 2, 1, 2, 1, 1, 2],
            y=["a", "a", "a", "a", "b", "b", "b", "b"],
            z=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5, 4.3, 7.7],
        )
        .group_by("x")
        .group_by("y")
    )

    expected = DataTable(x=[], y=[], z=[]).group_by("x").group_by("y")

    actual = table.slice0([])
    assert actual == expected

    actual = table.slice1([])
    assert actual == expected


def test_slice_only_one_out_of_bounds():
    table = DataTable(x=[1, 2, 2, 1, 2], y=[3.5, 2.2, 6.7, 8.9, -1.1]).group_by("x")

    # General Exception because who know what will come out of Polars
    with pytest.raises(Exception):
        _ = table.slice0([1, 2])

    with pytest.raises(Exception):
        _ = table.slice1([2, 3])


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group_by(),
        DataTable().group_by().group_by(),
    ],
)
def test_slice_empty(table):
    actual = table.slice0([])
    assert actual == table

    actual = table.slice1([])
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group_by(),
        DataTable().group_by().group_by(),
    ],
)
def test_slice_empty_out_of_bounds(table):
    table = DataTable()

    # General Exception because who know what will come out of Polars
    with pytest.raises(Exception):
        _ = table.slice0([0])

    with pytest.raises(Exception):
        _ = table.slice1([1])


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
def test_slice_columnless(table, expected):
    actual = table.slice0([0, 1, 4])
    assert actual == expected

    actual = table.slice1([1, 2, 5])
    assert actual == expected


@pytest.mark.parametrize(
    "table",
    [
        DataTable.columnless(height=4),
        DataTable.columnless(height=4).group_by(),
        DataTable.columnless(height=4).group_by().group_by(),
    ],
)
def test_slice_columnless_out_of_bounds(table):
    with pytest.raises(IndexOutOfRange):
        _ = table.slice0([2, 4])

    with pytest.raises(IndexOutOfRange):
        _ = table.slice1([0, 2])


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[], y=[], z=[]),
        DataTable(x=[], y=[]).group_by(),
        DataTable(x=[]).group_by().group_by(),
    ],
)
def test_slice_rowless(table):
    table = DataTable(x=[], y=[], z=[])

    actual = table.slice0([])
    assert actual == table

    actual = table.slice1([])
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[], y=[], z=[]),
        DataTable(x=[], y=[]).group_by(),
        DataTable(x=[]).group_by().group_by(),
    ],
)
def test_slice_rowless_out_of_bounds(table):
    table = DataTable(x=[], y=[], z=[])

    # General Exception because who know what will come out of Polars
    with pytest.raises(Exception):
        _ = table.slice0([0])

    with pytest.raises(Exception):
        _ = table.slice1([1])
