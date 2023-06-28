import pytest

from tabeline import DataFrame
from tabeline.exceptions import GroupColumnError


def test_transmute():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True])
    actual = df.transmute(z="x + 1")
    expected = DataFrame(z=[1, 1, 2])
    assert actual == expected


def test_transmute_grouped():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=[3, 2, 4]).group_by("y", "x")
    actual = df.transmute(zz="z + 1")
    expected = DataFrame(y=[True, False, True], x=[0, 0, 1], zz=[4, 3, 5]).group_by("y", "x")
    assert actual == expected


def test_transmute_referencing_group():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=[3, 2, 4]).group_by("y", "x")
    actual = df.transmute(zz="x + 1")
    expected = DataFrame(y=[True, False, True], x=[0, 0, 1], zz=[1, 1, 2]).group_by("y", "x")
    assert actual == expected


def test_transmute_overwrite():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True])
    actual = df.transmute(x="x + 1")
    expected = DataFrame(x=[1, 1, 2])
    assert actual == expected


def test_transmute_overwrite_grouped():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=[3, 2, 4], a=[2.3, 4.5, 6.7]).group_by(
        "y", "x"
    )
    actual = df.transmute(z="z + 1")
    expected = DataFrame(y=[True, False, True], x=[0, 0, 1], z=[4, 3, 5]).group_by("y", "x")
    assert actual == expected


def test_transmute_overwrite_referencing_group():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=[3, 2, 4], a=[2.3, 4.5, 6.7]).group_by(
        "y", "x"
    )
    actual = df.transmute(z="x + 1")
    expected = DataFrame(y=[True, False, True], x=[0, 0, 1], z=[1, 1, 2]).group_by("y", "x")
    assert actual == expected


def test_transmute_reference_previous_mutator():
    df = DataFrame(x=[0, 0, 1])
    actual = df.transmute(y="x + 1", z="2*y")
    expected = DataFrame(y=[1, 1, 2], z=[2, 2, 4])
    assert actual == expected


def test_transmute_reference_previous_mutator_grouped():
    df = DataFrame(x=[0, 0, 1], a=[2.3, 4.5, 6.7]).group_by("x")
    actual = df.transmute(y="x + 1", z="2*y")
    expected = DataFrame(x=[0, 0, 1], y=[1, 1, 2], z=[2, 2, 4]).group_by("x")
    assert actual == expected


def test_transmute_broadcast_scalar():
    df = DataFrame(x=[0, 0, 1])
    actual = df.transmute(max_x="max(x)")
    expected = DataFrame(max_x=[1, 1, 1])
    assert actual == expected


def test_transmute_group_column():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True]).group_by("x")
    with pytest.raises(GroupColumnError):
        _ = df.transmute(x="x+1")


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_mutate_empty(df):
    actual = df.transmute()
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
    actual = df.transmute()
    assert actual == df


@pytest.mark.parametrize(
    "expression",
    [
        {"y": "y + 1"},
        {"y": "z + 1"},
        {"y": "row_index1()"},
    ],
)
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(y=[], z=[]),
        DataFrame(y=[], z=[]).group_by(),
        DataFrame(y=[], z=[]).group_by().group_by(),
        DataFrame(x=[], y=[], z=[]).group_by("x"),
        DataFrame(w=[], x=[], y=[], z=[]).group_by("w", "x"),
        DataFrame(w=[], x=[], y=[], z=[]).group_by("w").group_by("x"),
    ],
)
def test_transmute_rowless(expression, df):
    actual = df.transmute(**expression)
    expected = df.deselect("z")
    assert actual == expected
