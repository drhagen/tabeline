import pytest

from tabeline import DataFrame
from tabeline.exceptions import GroupColumnError


def test_group_by():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4]).group_by("x")
    assert df.group_levels == (("x",),)


def test_group_by_multiple_columns():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4]).group_by("x", "y")
    assert df.group_levels == (("x", "y"),)


def test_group_by_multiple_levels():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4]).group_by("x").group_by("y")
    assert df.group_levels == (("x",), ("y",))


def test_group_by_same_column_twice():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4]).group_by("x")
    with pytest.raises(GroupColumnError):
        _ = df.group_by("x")


def test_group_by_cluster():
    df = DataFrame(x=[1, 0, 1, 0], y=[3, 1, 2, 4])
    actual = df.group_by("x", order="cluster")
    expected = DataFrame(x=[1, 1, 0, 0], y=[3, 2, 1, 4]).group_by("x")
    assert actual == expected


def test_group_by_sort():
    df = DataFrame(x=[1, 0, 2, 1, 1], y=[2.1, 1.0, 0.0, 3.4, 2.1], z=[1, 2, 3, 4, 5])
    actual = df.group_by("x", order="sort")
    expected = DataFrame(
        x=[0, 1, 1, 1, 2], y=[1.0, 2.1, 3.4, 2.1, 0.0], z=[2, 1, 4, 5, 3]
    ).group_by("x")
    assert actual == expected
