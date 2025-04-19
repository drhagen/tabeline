import pytest

from tabeline import DataFrame


def test_distinct():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = df.distinct("x")
    expected = DataFrame(x=[0, 1], y=[1, 3])
    assert actual == expected


def test_distinct_unsorted():
    df = DataFrame(x=[1, 1, 0, 0], y=[1, 2, 3, 4])
    actual = df.distinct("x")
    expected = DataFrame(x=[1, 0], y=[1, 3])
    assert actual == expected


def test_empty_distinct():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = df.distinct()
    expected = DataFrame(x=[0], y=[1])
    assert actual == expected


@pytest.mark.parametrize("distinct_columns", [["z"], ["x", "z"], ["z", "x"]])
def test_distinct_with_grouped_column(distinct_columns):
    df = DataFrame(
        x=[0, 0, 0, 1, 1, 1, 1], y=["a", "a", "b", "a", "a", "b", "b"], z=[1, 1, 1, 1, 2, 3, 3]
    ).group_by("x")
    actual = df.distinct(*distinct_columns)
    expected = DataFrame(x=[0, 1, 1, 1], y=["a", "a", "a", "b"], z=[1, 1, 2, 3]).group_by("x")
    assert actual == expected


@pytest.mark.parametrize("distinct_columns", [["z"], ["y", "z"], ["x", "z"]])
def test_distinct_with_two_grouped_columns(distinct_columns):
    df = DataFrame(
        x=[0, 0, 0, 1, 1, 1, 1], y=["a", "a", "b", "a", "a", "b", "b"], z=[1, 1, 1, 1, 2, 3, 3]
    ).group_by("x", "y")
    actual = df.distinct(*distinct_columns)
    expected = DataFrame(
        x=[0, 0, 1, 1, 1], y=["a", "b", "a", "a", "b"], z=[1, 1, 1, 2, 3]
    ).group_by("x", "y")
    assert actual == expected


@pytest.mark.parametrize("distinct_columns", [["z"], ["y", "z"], ["x", "z"]])
def test_distinct_with_two_separate_grouped_columns(distinct_columns):
    df = (
        DataFrame(
            x=[0, 0, 0, 1, 1, 1, 1], y=["a", "a", "b", "a", "a", "b", "b"], z=[1, 1, 1, 1, 2, 3, 3]
        )
        .group_by("x")
        .group_by("y")
    )
    actual = df.distinct(*distinct_columns)
    expected = (
        DataFrame(x=[0, 0, 1, 1, 1], y=["a", "b", "a", "a", "b"], z=[1, 1, 1, 2, 3])
        .group_by("x")
        .group_by("y")
    )
    assert actual == expected


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_distinct_on_empty(df):
    actual = df.distinct()
    assert actual == df


@pytest.mark.parametrize("columns", [[], ["x"], ["x", "y"], ["y", "x"]])
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[], y=[], z=[]),
        DataFrame(x=[], y=[]).group_by(),
        DataFrame(x=[], y=[]).group_by().group_by(),
    ],
)
def test_distinct_on_rowless(columns, df):
    actual = df.distinct(*columns)
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame.columnless(height=6),
        DataFrame.columnless(height=6).group_by(),
        DataFrame.columnless(height=6).group_by().group_by(),
    ],
)
def test_distinct_on_columnless(df):
    actual = df.distinct()
    assert actual.height == 1
    assert actual.width == 0
    assert actual.group_levels == df.group_levels
