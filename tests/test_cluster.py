import pytest

from tabeline import DataFrame


def test_cluster():
    df = DataFrame(x=[1, 0, 1, 0], y=[3, 1, 2, 4])
    actual = df.cluster("x")
    expected = DataFrame(x=[1, 1, 0, 0], y=[3, 2, 1, 4])
    assert actual == expected


def test_cluster_two():
    df = DataFrame(x=[2, 2, 1, 1, 2, 2], y=[3, 4, 4, 3, 4, 3], z=[1, 2, 3, 4, 5, 6])
    actual = df.cluster("x", "y")
    expected = DataFrame(x=[2, 2, 2, 2, 1, 1], y=[3, 3, 4, 4, 4, 3], z=[1, 6, 2, 5, 3, 4])
    assert actual == expected


def test_cluster_grouped():
    df = DataFrame(x=[2, 2, 1, 1, 2, 2], y=[3, 4, 4, 3, 4, 3], z=[1, 2, 3, 4, 5, 6]).group_by("x")
    actual = df.cluster("y")
    expected = DataFrame(
        x=[2, 2, 1, 1, 2, 2], y=[3, 3, 4, 3, 4, 4], z=[1, 6, 3, 4, 2, 5]
    ).group_by("x")
    assert actual == expected


def test_cluster_grouped_two():
    df = DataFrame(
        x=[2, 2, 1, 1, 2, 2, 2], y=[3, 4, 4, 4, 4, 3, 4], z=[2, 1, 1, 1, 2, 1, 1]
    ).group_by("x", "y")
    actual = df.cluster("z")
    expected = DataFrame(
        x=[2, 2, 1, 1, 2, 2, 2], y=[3, 4, 4, 4, 4, 3, 4], z=[2, 1, 1, 1, 1, 1, 2]
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
def test_cluster_empty(df):
    actual = df.cluster()
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame.columnless(height=6),
        DataFrame.columnless(height=6).group_by(),
        DataFrame.columnless(height=6).group_by().group_by(),
    ],
)
def test_cluster_columnless(df):
    actual = df.cluster()
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
def test_cluster_rowless(columns, df):
    actual = df.cluster()
    assert actual == df
