import pytest

from tabeline import DataTable
from tabeline.exceptions import NonexistentColumn, RenameExisting

swappers = [{"x": "y", "y": "x"}, {"y": "x", "x": "y"}]


def test_rename():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = table.rename(yy="y")
    expected = DataTable(x=[0, 0, 1], yy=[True, False, True], z=["a", "b", "c"])
    assert actual == expected


def test_rename_multiple():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = table.rename(xx="x", yy="y")
    expected = DataTable(xx=[0, 0, 1], yy=[True, False, True], z=["a", "b", "c"])
    assert actual == expected


def test_rename_multiple_different_order():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = table.rename(yy="y", xx="x")
    expected = DataTable(xx=[0, 0, 1], yy=[True, False, True], z=["a", "b", "c"])
    assert actual == expected


@pytest.mark.parametrize("swappers", swappers)
def test_rename_swap(swappers):
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = table.rename(**swappers)
    expected = DataTable(y=[0, 0, 1], x=[True, False, True], z=["a", "b", "c"])
    assert actual == expected


@pytest.mark.parametrize("swappers", swappers)
def test_rename_swap_into_group(swappers):
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x")
    actual = table.rename(**swappers)
    expected = DataTable(y=[0, 0, 1], x=[True, False, True], z=["a", "b", "c"]).group("y")
    assert actual == expected


@pytest.mark.parametrize("swappers", swappers)
def test_rename_swap_within_group(swappers):
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x", "y")
    actual = table.rename(**swappers)
    expected = DataTable(y=[0, 0, 1], x=[True, False, True], z=["a", "b", "c"]).group("y", "x")
    assert actual == expected


@pytest.mark.parametrize("swappers", swappers)
def test_rename_swap_between_group_levels(swappers):
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x").group("y")
    actual = table.rename(**swappers)
    expected = (
        DataTable(y=[0, 0, 1], x=[True, False, True], z=["a", "b", "c"]).group("y").group("x")
    )
    assert actual == expected


def test_rename_earlier_group_column():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x", "y")
    actual = table.rename(xx="x")
    expected = DataTable(xx=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("xx", "y")
    assert actual == expected


def test_rename_later_group_column():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x", "y")
    actual = table.rename(yy="y")
    expected = DataTable(x=[0, 0, 1], yy=[True, False, True], z=["a", "b", "c"]).group("x", "yy")
    assert actual == expected


def test_rename_earlier_group_level():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x").group("y")
    actual = table.rename(xx="x")
    expected = (
        DataTable(xx=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("xx").group("y")
    )
    assert actual == expected


def test_rename_later_group_level():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x").group("y")
    actual = table.rename(yy="y")
    expected = (
        DataTable(x=[0, 0, 1], yy=[True, False, True], z=["a", "b", "c"]).group("x").group("yy")
    )
    assert actual == expected


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable(x=[0, 0, 1]),
        DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]),
        DataTable().group(),
        DataTable(x=[0, 0, 1]).group("x"),
        DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x"),
        DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x", "y"),
        DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x").group("y"),
    ],
)
def test_noop_rename(table: DataTable):
    actual = table.rename()
    assert actual == table


@pytest.mark.parametrize(
    "columns", [{"x": "x"}, {"y": "y"}, {"x": "x", "y": "y"}, {"y": "y", "x": "x"}]
)
@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]),
        DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x"),
        DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x", "y"),
        DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group("x").group("y"),
    ],
)
def test_rename_self(columns, table):
    actual = table.rename(**columns)
    assert actual == table


def test_rename_nonexistent():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])

    with pytest.raises(NonexistentColumn):
        _ = table.rename(aa="a")


def test_rename_existing():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])

    with pytest.raises(RenameExisting):
        _ = table.rename(x="y")
