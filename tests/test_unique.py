import pytest

from tabeline import DataFrame


def test_unique():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 3])
    actual = df.unique()
    expected = DataFrame(x=[0, 0, 1], y=[1, 2, 3])
    assert actual == expected


def test_unique_grouped():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group_by("x")
    actual = df.unique()
    expected = DataFrame(x=[0, 0, 1], y=[1, 2, 3]).group_by("x")
    assert actual == expected


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_unique_empty(df):
    actual = df.unique()
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[], y=[], z=[]),
        DataFrame(x=[], y=[]).group_by(),
        DataFrame(x=[], y=[]).group_by().group_by(),
    ],
)
def test_unique_rowless(df):
    actual = df.unique()
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame.columnless(height=6),
        DataFrame.columnless(height=6).group_by(),
        DataFrame.columnless(height=6).group_by().group_by(),
    ],
)
def test_unique_columnless(df):
    actual = df.unique()
    assert actual.height == 1
    assert actual.width == 0
    assert actual.group_levels == df.group_levels
