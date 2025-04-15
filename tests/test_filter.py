import pytest

from tabeline import DataFrame


def test_filter():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = df.filter("x == max(x)")
    expected = DataFrame(x=[1, 1], y=[3, 4])
    assert actual == expected


def test_grouped_filter():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group_by("x")
    actual = df.filter("y == max(y)")
    expected = DataFrame(x=[0, 1, 1], y=[2, 3, 3]).group_by("x")
    assert actual == expected


def test_filter_out_all_rows():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = df.filter("x == 2")
    expected = DataFrame(x=[], y=[])
    assert actual == expected


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 3]),
        DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group_by("x"),
        DataFrame(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3]).group_by("x", "y"),
        DataFrame(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3])
        .group_by("x")
        .group_by("y"),
    ],
)
def test_filter_true(df):
    actual = df.filter("True")
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 3]),
        DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 3]).group_by("x"),
        DataFrame(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3]).group_by("x", "y"),
        DataFrame(x=[0, 0, 1, 1], y=[True, False, False, True], z=[1, 2, 3, 3])
        .group_by("x")
        .group_by("y"),
    ],
)
def test_filter_false(df):
    actual = df.filter("False")
    assert actual.height == 0
    assert actual.column_names == df.column_names
    assert actual.group_levels == df.group_levels


@pytest.mark.parametrize("expression", ["True", "False", "row_index1() == 1"])
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_filter_empty(expression, df):
    actual = df.filter(expression)
    assert actual == df


@pytest.mark.parametrize(
    ("df", "expected"),
    [
        (DataFrame.columnless(height=6), DataFrame.columnless(height=3)),
        (DataFrame.columnless(height=6).group_by(), DataFrame.columnless(height=3).group_by()),
        (
            DataFrame.columnless(height=6).group_by().group_by(),
            DataFrame.columnless(height=3).group_by().group_by(),
        ),
    ],
)
def test_filter_columnless(df, expected):
    actual = df.filter("row_index0() % 2 == 0")
    assert actual == expected


@pytest.mark.parametrize("expression", ["True", "False", "row_index1() == 1"])
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[], y=[], z=[]),
        DataFrame(x=[], y=[]).group_by(),
        DataFrame(x=[]).group_by().group_by(),
        DataFrame(x=[], y=[], z=[]).group_by("x"),
        DataFrame(x=[], y=[], z=[]).group_by("x", "y"),
        DataFrame(x=[], y=[], z=[]).group_by("x").group_by("y"),
    ],
)
def test_filter_rowless(expression, df):
    actual = df.filter(expression)
    assert actual == df
