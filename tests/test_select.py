import pytest

from tabeline import DataTable
from tabeline.exceptions import NonexistentColumn


def test_select():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = table.select("x", "z")
    expected = DataTable(x=[0, 0, 1], z=["a", "b", "c"])
    assert actual == expected


test_columns = {
    "a": [1, 0, 1, 0],
    "b": ["a", "b", "b", "b"],
    "c": [True, True, True, False],
    "d": [3.4, 2.7, -9.0, 0.0],
}


@pytest.mark.parametrize(
    ["input_columns", "selectors"],
    [
        [["a", "b", "c"], ["a"]],
        [["a", "b", "c"], ["b"]],
        [["a", "b", "c"], ["c"]],
        [["a", "b", "c", "d"], ["b", "c"]],
        [["a", "b", "c", "d"], ["c", "b"]],
        [["a", "b", "c", "d"], ["a", "b", "c", "d"]],
        [["a", "b", "c", "d"], ["d", "b", "a", "c"]],
    ],
)
def test_select_columns(input_columns: list[str], selectors: list[str]):
    table = DataTable(**{name: test_columns[name] for name in input_columns})
    actual = table.select(*selectors)
    expected = DataTable(**{name: test_columns[name] for name in selectors})
    assert actual == expected


@pytest.mark.parametrize(
    "input_columns",
    [
        [],
        ["a"],
        ["a", "b"],
    ],
)
def test_select_no_columns(input_columns):
    table = DataTable(**{name: test_columns[name] for name in input_columns})
    actual = table.select()
    expected = DataTable.columnless(height=table.height)
    assert actual == expected


@pytest.mark.parametrize(
    ["input_columns", "groups", "selectors", "expected_columns"],
    [
        [[], [], [], []],
        [["a"], [["a"]], [], ["a"]],
        [["a", "b"], [["a", "b"]], [], ["a", "b"]],
        [["a", "b"], [["a"], ["b"]], [], ["a", "b"]],
        [["a"], [["a"]], ["a"], ["a"]],
        [["a", "b"], [["a", "b"]], ["b"], ["a", "b"]],
        [["a", "b"], [["a"], ["b"]], ["b"], ["a", "b"]],
        [["a", "b"], [["a", "b"]], ["a"], ["b", "a"]],
        [["a", "b"], [["a"], ["b"]], ["a"], ["b", "a"]],
        [["a", "b", "c", "d"], [["a", "b"]], ["c"], ["a", "b", "c"]],
        [["a", "b", "c", "d"], [["a", "b"]], ["a", "c"], ["b", "a", "c"]],
        [["a", "b", "c", "d"], [["a", "b"]], ["a", "b", "c"], ["a", "b", "c"]],
        [["a", "b", "c", "d"], [["b", "a"]], ["c"], ["a", "b", "c"]],
        [["a", "b", "c", "d"], [["b", "a"]], ["a", "c"], ["b", "a", "c"]],
        [["a", "b", "c", "d"], [["b", "a"]], ["b", "c"], ["a", "b", "c"]],
        [["a", "b", "c", "d"], [["b", "a"]], ["a", "b", "c"], ["a", "b", "c"]],
        [["a", "b", "c", "d"], [["b", "a"], []], ["a", "b", "c"], ["a", "b", "c"]],
        [["a", "b", "c", "d"], [["b"], ["a"]], ["a", "b", "c"], ["a", "b", "c"]],
        [["a", "b", "c", "d"], [[], ["b", "a"]], ["a", "b", "c"], ["a", "b", "c"]],
    ],
)
def test_select_columns_grouped(
    input_columns: list[str],
    groups: list[list[str]],
    selectors: list[str],
    expected_columns: list[str],
):
    table = DataTable(**{name: test_columns[name] for name in input_columns})
    for level in groups:
        table = table.group(*level)
    actual = table.select(*selectors)
    expected = DataTable(**{name: test_columns[name] for name in expected_columns})
    for level in groups:
        expected = expected.group(*level)
    assert actual == expected


def test_select_nonexistent_column():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])

    with pytest.raises(NonexistentColumn):
        _ = table.select("x", "a")


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group(),
        DataTable().group().group(),
    ],
)
def test_select_empty(table):
    actual = table.select()
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable.columnless(height=6),
        DataTable.columnless(height=6).group(),
        DataTable.columnless(height=6).group().group(),
    ],
)
def test_select_columnless(table):
    actual = table.select()
    assert actual == table
