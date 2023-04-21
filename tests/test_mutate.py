import pytest

from tabeline import DataTable
from tabeline.exceptions import GroupColumn


def test_mutate():
    table = DataTable(x=[0, 0, 1], y=[True, False, True])
    actual = table.mutate(z="x + 1")
    expected = DataTable(x=[0, 0, 1], y=[True, False, True], z=[1, 1, 2])
    assert actual == expected


def test_mutate_grouped():
    table = DataTable(x=[True, False, True], y=[0, 0, 1]).group_by("x")
    actual = table.mutate(z="y + 1")
    expected = DataTable(x=[True, False, True], y=[0, 0, 1], z=[1, 1, 2]).group_by("x")
    assert actual == expected


def test_mutate_referencing_group():
    table = DataTable(x=[True, False, True], y=[0, 0, 1]).group_by("x")
    actual = table.mutate(z="~x")
    expected = DataTable(x=[True, False, True], y=[0, 0, 1], z=[False, True, False]).group_by("x")
    assert actual == expected


def test_mutate_overwrite():
    table = DataTable(x=[0, 0, 1], y=[True, False, True])
    actual = table.mutate(x="x + 1")
    expected = DataTable(x=[1, 1, 2], y=[True, False, True])
    assert actual == expected


def test_mutate_overwrite_grouped():
    table = DataTable(x=[True, False, True], y=[0, 0, 1]).group_by("x")
    actual = table.mutate(y="y + 1")
    expected = DataTable(x=[True, False, True], y=[1, 1, 2]).group_by("x")
    assert actual == expected


def test_mutate_overwrite_referencing_group():
    table = DataTable(x=[True, False, True], y=[0, 0, 1]).group_by("x")
    actual = table.mutate(y="~x")
    expected = DataTable(x=[True, False, True], y=[False, True, False]).group_by("x")
    assert actual == expected


def test_mutate_reference_previous_mutator():
    table = DataTable(x=[0, 0, 1])
    actual = table.mutate(y="x + 1", z="2*y")
    expected = DataTable(x=[0, 0, 1], y=[1, 1, 2], z=[2, 2, 4])
    assert actual == expected


def test_mutate_reference_previous_mutator_grouped():
    table = DataTable(x=[0, 0, 1]).group_by("x")
    actual = table.mutate(y="max(x)", z="y+1")
    expected = DataTable(x=[0, 0, 1], y=[0, 0, 1], z=[1, 1, 2]).group_by("x")
    assert actual == expected


def test_mutate_broadcast_scalar():
    table = DataTable(x=[0, 0, 1])
    actual = table.mutate(max_x="max(x)")
    expected = DataTable(x=[0, 0, 1], max_x=[1, 1, 1])
    assert actual == expected


def test_mutate_group_column():
    table = DataTable(x=[0, 0, 1], y=[True, False, True]).group_by("x")
    with pytest.raises(GroupColumn):
        _ = table.mutate(x="x+1")


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group_by(),
        DataTable().group_by().group_by(),
    ],
)
def test_mutate_empty(table):
    actual = table.mutate()
    assert actual == table


@pytest.mark.parametrize(
    "table",
    [
        DataTable.columnless(height=6),
        DataTable.columnless(height=6).group_by(),
        DataTable.columnless(height=6).group_by().group_by(),
    ],
)
def test_mutate_columnless(table):
    actual = table.mutate()
    assert actual == table


@pytest.mark.parametrize(
    "expression",
    [
        {"w": "w + 1"},
        {"z": "x + 1"},
        {"w": "row_index1() + 1"},
        {"w": "1", "z": "w + 1"},
    ],
)
@pytest.mark.parametrize(
    "table",
    [
        DataTable(w=[], x=[], y=[], z=[]),
        DataTable(w=[], x=[], y=[], z=[]).group_by(),
        DataTable(w=[], x=[], y=[], z=[]).group_by().group_by(),
        DataTable(w=[], x=[], y=[], z=[]).group_by("x"),
        DataTable(w=[], x=[], y=[], z=[]).group_by("x", "y"),
        DataTable(w=[], x=[], y=[], z=[]).group_by("x").group_by("y"),
    ],
)
def test_mutate_rowless(expression, table):
    actual = table.mutate(**expression)
    assert actual == table
