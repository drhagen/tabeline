import pytest

from tabeline import DataFrame
from tabeline.exceptions import GroupColumnError


def test_mutate():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True])
    actual = df.mutate(z="x + 1")
    expected = DataFrame(x=[0, 0, 1], y=[True, False, True], z=[1, 1, 2])
    assert actual == expected


def test_mutate_grouped():
    df = DataFrame(x=[True, False, True], y=[0, 0, 1]).group_by("x")
    actual = df.mutate(z="y + 1")
    expected = DataFrame(x=[True, False, True], y=[0, 0, 1], z=[1, 1, 2]).group_by("x")
    assert actual == expected


def test_mutate_referencing_group():
    df = DataFrame(x=[True, False, True], y=[0, 0, 1]).group_by("x")
    actual = df.mutate(z="~x")
    expected = DataFrame(x=[True, False, True], y=[0, 0, 1], z=[False, True, False]).group_by("x")
    assert actual == expected


def test_mutate_overwrite():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True])
    actual = df.mutate(x="x + 1")
    expected = DataFrame(x=[1, 1, 2], y=[True, False, True])
    assert actual == expected


def test_mutate_overwrite_grouped():
    df = DataFrame(x=[True, False, True], y=[0, 0, 1]).group_by("x")
    actual = df.mutate(y="y + 1")
    expected = DataFrame(x=[True, False, True], y=[1, 1, 2]).group_by("x")
    assert actual == expected


def test_mutate_overwrite_referencing_group():
    df = DataFrame(x=[True, False, True], y=[0, 0, 1]).group_by("x")
    actual = df.mutate(y="~x")
    expected = DataFrame(x=[True, False, True], y=[False, True, False]).group_by("x")
    assert actual == expected


def test_mutate_reference_previous_mutator():
    df = DataFrame(x=[0, 0, 1])
    actual = df.mutate(y="x + 1", z="2*y")
    expected = DataFrame(x=[0, 0, 1], y=[1, 1, 2], z=[2, 2, 4])
    assert actual == expected


def test_mutate_reference_previous_mutator_grouped():
    df = DataFrame(x=[0, 0, 1]).group_by("x")
    actual = df.mutate(y="max(x)", z="y+1")
    expected = DataFrame(x=[0, 0, 1], y=[0, 0, 1], z=[1, 1, 2]).group_by("x")
    assert actual == expected


def test_mutate_broadcast_scalar():
    df = DataFrame(x=[0, 0, 1])
    actual = df.mutate(max_x="max(x)")
    expected = DataFrame(x=[0, 0, 1], max_x=[1, 1, 1])
    assert actual == expected


def test_mutate_group_column():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True]).group_by("x")
    with pytest.raises(GroupColumnError):
        _ = df.mutate(x="x+1")


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_mutate_empty(df):
    actual = df.mutate()
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame.columnless(height=6),
        DataFrame.columnless(height=6).group_by(),
        DataFrame.columnless(height=6).group_by().group_by(),
    ],
)
def test_mutate_columnless(df):
    actual = df.mutate()
    assert actual == df


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
    "df",
    [
        DataFrame(w=[], x=[], y=[], z=[]),
        DataFrame(w=[], x=[], y=[], z=[]).group_by(),
        DataFrame(w=[], x=[], y=[], z=[]).group_by().group_by(),
        DataFrame(w=[], x=[], y=[], z=[]).group_by("x"),
        DataFrame(w=[], x=[], y=[], z=[]).group_by("x", "y"),
        DataFrame(w=[], x=[], y=[], z=[]).group_by("x").group_by("y"),
    ],
)
def test_mutate_rowless(expression, df):
    actual = df.mutate(**expression)
    assert actual == df
