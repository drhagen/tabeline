import pytest

from tabeline import DataFrame


def test_sort():
    df = DataFrame(x=[1, 0, 2, 1, 1], y=[2.1, 1.0, 0.0, 3.4, 2.1], z=[1, 2, 3, 4, 5])
    actual = df.sort("x")
    expected = DataFrame(x=[0, 1, 1, 1, 2], y=[1.0, 2.1, 3.4, 2.1, 0.0], z=[2, 1, 4, 5, 3])
    assert actual == expected


def test_sort_two():
    df = DataFrame(x=[1, 0, 2, 1, 1], y=[2.1, 1.0, 0.0, 3.4, 2.1], z=[1, 2, 3, 4, 5])
    actual = df.sort("x", "y")
    expected = DataFrame(x=[0, 1, 1, 1, 2], y=[1.0, 2.1, 2.1, 3.4, 0.0], z=[2, 1, 5, 4, 3])
    assert actual == expected


def test_sort_grouped():
    df = DataFrame(x=[2, 2, 1, 1, 2, 2], y=[3, 4, 3, 1, 1, 3], z=[5, 4, 3, 2, 1, 0]).group_by("x")
    actual = df.sort("y")
    expected = DataFrame(
        x=[2, 2, 1, 1, 2, 2], y=[1, 3, 1, 3, 3, 4], z=[1, 5, 2, 3, 0, 4]
    ).group_by("x")
    assert actual == expected


def test_sort_two_grouped():
    df = DataFrame(x=[2, 2, 1, 1, 2, 2], y=[3, 4, 3, 1, 1, 3], z=[5, 4, 3, 2, 1, 0]).group_by("x")
    actual = df.sort("y", "z")
    expected = DataFrame(
        x=[2, 2, 1, 1, 2, 2], y=[1, 3, 1, 3, 3, 4], z=[1, 0, 2, 3, 5, 4]
    ).group_by("x")
    assert actual == expected


def test_sort_grouped_two():
    df = DataFrame(x=[2, 2, 1, 1, 2, 2], y=[3, 3, 3, 1, 1, 3], z=[5, 4, 3, 2, 1, 0]).group_by(
        "x", "y"
    )
    actual = df.sort("z")
    expected = DataFrame(
        x=[2, 2, 1, 1, 2, 2], y=[3, 3, 3, 1, 1, 3], z=[0, 4, 3, 2, 1, 5]
    ).group_by("x", "y")
    assert actual == expected


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_sort_empty(df):
    actual = df.sort()
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame.columnless(height=6),
        DataFrame.columnless(height=6).group_by(),
        DataFrame.columnless(height=6).group_by().group_by(),
    ],
)
def test_sort_columnless(df):
    actual = df.sort()
    assert actual == df


@pytest.mark.parametrize("columns", [[], ["z"], ["z", "y"], ["y", "z"]])
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[], y=[], z=[]),
        DataFrame(x=[], y=[], z=[]).group_by(),
        DataFrame(x=[], y=[], z=[]).group_by().group_by(),
        DataFrame(x=[], y=[], z=[]).group_by("x"),
        DataFrame(w=[], x=[], y=[], z=[]).group_by("w").group_by("x"),
        DataFrame(w=[], x=[], y=[], z=[]).group_by("x", "w"),
    ],
)
def test_sort_rowless(columns, df):
    actual = df.sort()
    assert actual == df
