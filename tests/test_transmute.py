import pytest

from tabeline import DataTable
from tabeline.exceptions import GroupColumn


def test_transmute():
    table = DataTable(x=[0, 0, 1], y=[True, False, True])
    actual = table.transmute(z="x + 1")
    expected = DataTable(z=[1, 1, 2])
    assert actual == expected


def test_transmute_grouped():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=[3, 2, 4]).group_by("y", "x")
    actual = table.transmute(zz="z + 1")
    expected = DataTable(y=[True, False, True], x=[0, 0, 1], zz=[4, 3, 5]).group_by("y", "x")
    assert actual == expected


def test_transmute_referencing_group():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=[3, 2, 4]).group_by("y", "x")
    actual = table.transmute(zz="x + 1")
    expected = DataTable(y=[True, False, True], x=[0, 0, 1], zz=[1, 1, 2]).group_by("y", "x")
    assert actual == expected


def test_transmute_overwrite():
    table = DataTable(x=[0, 0, 1], y=[True, False, True])
    actual = table.transmute(x="x + 1")
    expected = DataTable(x=[1, 1, 2])
    assert actual == expected


def test_transmute_overwrite_grouped():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=[3, 2, 4], a=[2.3, 4.5, 6.7]).group_by(
        "y", "x"
    )
    actual = table.transmute(z="z + 1")
    expected = DataTable(y=[True, False, True], x=[0, 0, 1], z=[4, 3, 5]).group_by("y", "x")
    assert actual == expected


def test_transmute_overwrite_referencing_group():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=[3, 2, 4], a=[2.3, 4.5, 6.7]).group_by(
        "y", "x"
    )
    actual = table.transmute(z="x + 1")
    expected = DataTable(y=[True, False, True], x=[0, 0, 1], z=[1, 1, 2]).group_by("y", "x")
    assert actual == expected


def test_transmute_reference_previous_mutator():
    table = DataTable(x=[0, 0, 1])
    actual = table.transmute(y="x + 1", z="2*y")
    expected = DataTable(y=[1, 1, 2], z=[2, 2, 4])
    assert actual == expected


def test_transmute_reference_previous_mutator_grouped():
    table = DataTable(x=[0, 0, 1], a=[2.3, 4.5, 6.7]).group_by("x")
    actual = table.transmute(y="x + 1", z="2*y")
    expected = DataTable(x=[0, 0, 1], y=[1, 1, 2], z=[2, 2, 4]).group_by("x")
    assert actual == expected


def test_transmute_broadcast_scalar():
    table = DataTable(x=[0, 0, 1])
    actual = table.transmute(max_x="max(x)")
    expected = DataTable(max_x=[1, 1, 1])
    assert actual == expected


def test_transmute_group_column():
    table = DataTable(x=[0, 0, 1], y=[True, False, True]).group_by("x")
    with pytest.raises(GroupColumn):
        _ = table.transmute(x="x+1")


@pytest.mark.parametrize(
    "table",
    [
        DataTable(),
        DataTable().group_by(),
        DataTable().group_by().group_by(),
    ],
)
def test_mutate_empty(table):
    actual = table.transmute()
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
    actual = table.transmute()
    assert actual == table


@pytest.mark.parametrize(
    "expression",
    [
        {"y": "y + 1"},
        {"y": "z + 1"},
        {"y": "row_index1()"},
    ],
)
@pytest.mark.parametrize(
    "table",
    [
        DataTable(y=[], z=[]),
        DataTable(y=[], z=[]).group_by(),
        DataTable(y=[], z=[]).group_by().group_by(),
        DataTable(x=[], y=[], z=[]).group_by("x"),
        DataTable(w=[], x=[], y=[], z=[]).group_by("w", "x"),
        DataTable(w=[], x=[], y=[], z=[]).group_by("w").group_by("x"),
    ],
)
def test_transmute_rowless(expression, table):
    actual = table.transmute(**expression)
    expected = table.deselect("z")
    assert actual == expected
