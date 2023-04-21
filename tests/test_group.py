import pytest

from tabeline import DataTable
from tabeline.exceptions import GroupColumn


def test_group_by():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4]).group_by("x")
    assert table.group_levels == (("x",),)


def test_group_by_multiple_columns():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4]).group_by("x", "y")
    assert table.group_levels == (("x", "y"),)


def test_group_by_multiple_levels():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4]).group_by("x").group_by("y")
    assert table.group_levels == (("x",), ("y",))


def test_group_by_same_column_twice():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4]).group_by("x")
    with pytest.raises(GroupColumn):
        _ = table.group_by("x")


def test_group_by_cluster():
    table = DataTable(x=[1, 0, 1, 0], y=[3, 1, 2, 4])
    actual = table.group_by("x", order="cluster")
    expected = DataTable(x=[1, 1, 0, 0], y=[3, 2, 1, 4]).group_by("x")
    assert actual == expected


def test_group_by_sort():
    table = DataTable(x=[1, 0, 2, 1, 1], y=[2.1, 1.0, 0.0, 3.4, 2.1], z=[1, 2, 3, 4, 5])
    actual = table.group_by("x", order="sort")
    expected = DataTable(
        x=[0, 1, 1, 1, 2], y=[1.0, 2.1, 3.4, 2.1, 0.0], z=[2, 1, 4, 5, 3]
    ).group_by("x")
    assert actual == expected
