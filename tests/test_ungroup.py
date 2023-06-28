import pytest

from tabeline import DataFrame
from tabeline.exceptions import NoGroupsError


def test_ungroup():
    actual = (
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group_by("x").group_by("y").ungroup()
    )
    expected = DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group_by("x")
    assert actual == expected


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group_by().ungroup(),
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group_by("x").ungroup(),
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group_by("x", "y").ungroup(),
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"])
        .group_by()
        .group_by()
        .ungroup()
        .ungroup(),
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"])
        .group_by("x")
        .group_by("y")
        .ungroup()
        .ungroup(),
    ],
)
def test_ungroup_completely(df):
    assert df.group_levels == ()


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group_by("x").group_by("y").ungroup(),
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"])
        .group_by("x")
        .group_by()
        .group_by("y")
        .ungroup()
        .ungroup(),
    ],
)
def test_ungroup_to_one_level(df):
    assert df.group_levels == (("x",),)


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]),
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group_by("x").ungroup(),
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"]).group_by("x", "y").ungroup(),
        DataFrame(x=[0, 0, 1, 1], y=["a", "b", "b", "b"])
        .group_by("y")
        .group_by("x")
        .ungroup()
        .ungroup(),
    ],
)
def test_ungroup_no_groups(df):
    with pytest.raises(NoGroupsError):
        _ = df.ungroup()
