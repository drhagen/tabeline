from typing import Any

import pytest

from tabeline import DataTable
from tabeline.exceptions import GroupColumn, NonexistentColumn


def test_deselect():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = table.deselect("x", "z")
    expected = DataTable(y=[True, False, True])
    assert actual == expected


full_columns = {
    "a": [1, 0, 1, 0],
    "b": ["a", "b", "b", "b"],
    "c": [True, True, True, False],
    "d": [3.4, 2.7, -9.0, 0.0],
}

empty_columns = {
    "a": [],
    "b": [],
    "c": [],
    "d": [],
}


@pytest.mark.parametrize("test_columns", [full_columns, empty_columns])
@pytest.mark.parametrize(
    ["input_columns", "deselectors", "expected_columns"],
    [
        [[], [], []],
        [["a"], [], ["a"]],
        [["a", "b"], ["a"], ["b"]],
        [["a", "b", "c"], ["a", "c"], ["b"]],
        [["a", "b", "c"], ["c", "a"], ["b"]],
        [["a", "b", "c"], ["b", "c", "a"], []],
        [["a", "b", "c", "d"], ["c", "a"], ["b", "d"]],
    ],
)
def test_deselect_columns(
    input_columns: list[str],
    deselectors: list[str],
    expected_columns: list[str],
    test_columns: dict[str, Any],
):
    table = DataTable(**{name: full_columns[name] for name in input_columns})
    actual = table.deselect(*deselectors)
    if len(expected_columns) == 0:
        expected = DataTable.columnless(height=table.height)
    else:
        expected = DataTable(**{name: full_columns[name] for name in expected_columns})
    assert actual == expected


def test_deselect_nonexistent_column():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])

    with pytest.raises(NonexistentColumn):
        _ = table.deselect("x", "a")


def test_deselect_group_column():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x")

    with pytest.raises(GroupColumn):
        _ = table.deselect("x")


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group(),
        DataTable().group().group(),
    ],
)
def test_deselect_empty(table):
    actual = table.deselect()
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable.columnless(height=6),
        DataTable.columnless(height=6).group(),
        DataTable.columnless(height=6).group().group(),
    ],
)
def test_deselect_columnless(table):
    actual = table.deselect()
    assert actual == table
