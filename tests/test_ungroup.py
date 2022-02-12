import pytest

from tabeline import DataTable
from tabeline.exceptions import NoGroups


def test_ungroup():
    actual = DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group("x").group("y").ungroup()
    expected = DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group("x")
    assert actual == expected


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group().ungroup(),
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group("x").ungroup(),
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group("x", "y").ungroup(),
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group().group().ungroup().ungroup(),
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"])
        .group("x")
        .group("y")
        .ungroup()
        .ungroup(),
    ],
)
def test_ungroup_completely(table):
    assert table.group_levels == ()


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group("x").group("y").ungroup(),
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"])
        .group("x")
        .group()
        .group("y")
        .ungroup()
        .ungroup(),
    ],
)
def test_ungroup_to_one_level(table):
    assert table.group_levels == (("x",),)


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]),
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group("x").ungroup(),
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group("x", "y").ungroup(),
        DataTable(x=[0, 0, 1, 1], y=["a", "b", "b", "b"])
        .group("y")
        .group("x")
        .ungroup()
        .ungroup(),
    ],
)
def test_ungroup_no_groups(table):
    with pytest.raises(NoGroups):
        _ = table.ungroup()
