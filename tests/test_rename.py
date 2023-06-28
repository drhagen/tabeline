import pytest

from tabeline import DataFrame
from tabeline.exceptions import NonexistentColumnError, RenameExistingError

swappers = [{"x": "y", "y": "x"}, {"y": "x", "x": "y"}]


def test_rename():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = df.rename(yy="y")
    expected = DataFrame(x=[0, 0, 1], yy=[True, False, True], z=["a", "b", "c"])
    assert actual == expected


def test_rename_multiple():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = df.rename(xx="x", yy="y")
    expected = DataFrame(xx=[0, 0, 1], yy=[True, False, True], z=["a", "b", "c"])
    assert actual == expected


def test_rename_multiple_different_order():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = df.rename(yy="y", xx="x")
    expected = DataFrame(xx=[0, 0, 1], yy=[True, False, True], z=["a", "b", "c"])
    assert actual == expected


@pytest.mark.parametrize("swappers", swappers)
def test_rename_swap(swappers):
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = df.rename(**swappers)
    expected = DataFrame(y=[0, 0, 1], x=[True, False, True], z=["a", "b", "c"])
    assert actual == expected


@pytest.mark.parametrize("swappers", swappers)
def test_rename_swap_into_group(swappers):
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x")
    actual = df.rename(**swappers)
    expected = DataFrame(y=[0, 0, 1], x=[True, False, True], z=["a", "b", "c"]).group_by("y")
    assert actual == expected


@pytest.mark.parametrize("swappers", swappers)
def test_rename_swap_within_group(swappers):
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x", "y")
    actual = df.rename(**swappers)
    expected = DataFrame(y=[0, 0, 1], x=[True, False, True], z=["a", "b", "c"]).group_by("y", "x")
    assert actual == expected


@pytest.mark.parametrize("swappers", swappers)
def test_rename_swap_between_group_levels(swappers):
    df = (
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
        .group_by("x")
        .group_by("y")
    )
    actual = df.rename(**swappers)
    expected = (
        DataFrame(y=[0, 0, 1], x=[True, False, True], z=["a", "b", "c"])
        .group_by("y")
        .group_by("x")
    )
    assert actual == expected


def test_rename_earlier_group_column():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x", "y")
    actual = df.rename(xx="x")
    expected = DataFrame(xx=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by(
        "xx", "y"
    )
    assert actual == expected


def test_rename_later_group_column():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x", "y")
    actual = df.rename(yy="y")
    expected = DataFrame(x=[0, 0, 1], yy=[True, False, True], z=["a", "b", "c"]).group_by(
        "x", "yy"
    )
    assert actual == expected


def test_rename_earlier_group_level():
    df = (
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
        .group_by("x")
        .group_by("y")
    )
    actual = df.rename(xx="x")
    expected = (
        DataFrame(xx=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
        .group_by("xx")
        .group_by("y")
    )
    assert actual == expected


def test_rename_later_group_level():
    df = (
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
        .group_by("x")
        .group_by("y")
    )
    actual = df.rename(yy="y")
    expected = (
        DataFrame(x=[0, 0, 1], yy=[True, False, True], z=["a", "b", "c"])
        .group_by("x")
        .group_by("yy")
    )
    assert actual == expected


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame(x=[0, 0, 1]),
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]),
        DataFrame().group_by(),
        DataFrame(x=[0, 0, 1]).group_by("x"),
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x"),
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x", "y"),
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
        .group_by("x")
        .group_by("y"),
    ],
)
def test_noop_rename(df: DataFrame):
    actual = df.rename()
    assert actual == df


@pytest.mark.parametrize(
    "columns", [{"x": "x"}, {"y": "y"}, {"x": "x", "y": "y"}, {"y": "y", "x": "x"}]
)
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]),
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x"),
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x", "y"),
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
        .group_by("x")
        .group_by("y"),
    ],
)
def test_rename_self(columns, df):
    actual = df.rename(**columns)
    assert actual == df


def test_rename_nonexistent():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])

    with pytest.raises(NonexistentColumnError):
        _ = df.rename(aa="a")


def test_rename_existing():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])

    with pytest.raises(RenameExistingError):
        _ = df.rename(x="y")
