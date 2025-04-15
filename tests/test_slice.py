import pytest

from tabeline import DataFrame
from tabeline.exceptions import GroupIndexOutOfBoundsError, IndexOutOfBoundsError


def test_slice():
    df = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])

    expected = DataFrame(x=[1, 3], y=[True, True], z=[3.5, 6.7])

    actual = df.slice0([0, 2])
    assert actual == expected

    actual = df.slice1([1, 3])
    assert actual == expected


def test_slice_out_of_bounds():
    df = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])

    with pytest.raises(IndexOutOfBoundsError):
        _ = df.slice0([2, 4])

    with pytest.raises(IndexOutOfBoundsError):
        _ = df.slice1([0, 2])


def test_slice_groups():
    df = DataFrame(x=[1, 2, 2, 1, 2, 1], y=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5]).group_by("x")

    expected = DataFrame(x=[2, 1, 2, 1], y=[6.7, 8.9, -1.1, 4.5]).group_by("x")

    actual = df.slice0([1, 2])
    assert actual == expected

    actual = df.slice1([2, 3])
    assert actual == expected


def test_slice_one_index():
    df = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])

    expected = DataFrame(x=[1], y=[True], z=[3.5])

    actual = df.slice0([0])
    assert actual == expected

    actual = df.slice1([1])
    assert actual == expected


def test_slice_groups_one_index():
    df = DataFrame(x=[1, 2, 2, 1, 2, 1], y=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5]).group_by("x")

    expected = DataFrame(x=[2, 1], y=[6.7, 8.9]).group_by("x")

    actual = df.slice0([1])
    assert actual == expected

    actual = df.slice1([2])
    assert actual == expected


def test_slice_groups_multiple_columns_one_index():
    df = (
        DataFrame(
            x=[1, 2, 2, 1, 2, 1, 1, 2],
            y=["a", "a", "a", "a", "b", "b", "b", "b"],
            z=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5, 4.3, 7.7],
        )
        .group_by("x")
        .group_by("y")
    )

    expected = (
        DataFrame(x=[2, 1, 1, 2], y=["a", "a", "b", "b"], z=[6.7, 8.9, 4.3, 7.7])
        .group_by("x")
        .group_by("y")
    )

    actual = df.slice0([1])
    assert actual == expected

    actual = df.slice1([2])
    assert actual == expected


def test_slice_to_nothing():
    df = DataFrame(x=[1, 2, 2, 1, 2, 1], y=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5])

    expected = DataFrame(x=[], y=[])

    actual = df.slice0([])
    assert actual == expected

    actual = df.slice1([])
    assert actual == expected


def test_slice_groups_to_nothing():
    df = DataFrame(x=[1, 2, 2, 1, 2, 1], y=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5]).group_by("x")

    expected = DataFrame(x=[], y=[]).group_by("x")

    actual = df.slice0([])
    assert actual == expected

    actual = df.slice1([])
    assert actual == expected


def test_slice_multiple_groups_to_nothing():
    df = (
        DataFrame(
            x=[1, 2, 2, 1, 2, 1, 1, 2],
            y=["a", "a", "a", "a", "b", "b", "b", "b"],
            z=[3.5, 2.2, 6.7, 8.9, -1.1, 4.5, 4.3, 7.7],
        )
        .group_by("x")
        .group_by("y")
    )

    expected = DataFrame(x=[], y=[], z=[]).group_by("x").group_by("y")

    actual = df.slice0([])
    assert actual == expected

    actual = df.slice1([])
    assert actual == expected


def test_slice_only_one_out_of_bounds():
    df = DataFrame(x=[1, 2, 2, 1, 2], y=[3.5, 2.2, 6.7, 8.9, -1.1]).group_by("x")

    # Cannot control what comes out of Polars when grouping, so check some kind of error
    with pytest.raises((IndexOutOfBoundsError, GroupIndexOutOfBoundsError)):
        _ = df.slice0([1, 2])

    with pytest.raises((IndexOutOfBoundsError, GroupIndexOutOfBoundsError)):
        _ = df.slice1([2, 3])


def test_slice_negative_grouped():
    df = DataFrame(x=[1, 2, 2, 1, 2], y=[3.5, 2.2, 6.7, 8.9, -1.1]).group_by("x")

    with pytest.raises(IndexOutOfBoundsError):
        _ = df.slice0([-1, 0])

    with pytest.raises(IndexOutOfBoundsError):
        _ = df.slice1([0, 1])


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_slice_empty(df):
    actual = df.slice0([])
    assert actual == df

    actual = df.slice1([])
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_slice_empty_out_of_bounds(df):
    df = DataFrame()

    with pytest.raises(IndexOutOfBoundsError):
        _ = df.slice0([0])

    with pytest.raises(IndexOutOfBoundsError):
        _ = df.slice1([1])


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
def test_slice_columnless(df, expected):
    actual = df.slice0([0, 1, 4])
    assert actual == expected

    actual = df.slice1([1, 2, 5])
    assert actual == expected


@pytest.mark.parametrize(
    "df",
    [
        DataFrame.columnless(height=4),
        DataFrame.columnless(height=4).group_by(),
        DataFrame.columnless(height=4).group_by().group_by(),
    ],
)
def test_slice_columnless_out_of_bounds(df):
    with pytest.raises((IndexOutOfBoundsError, GroupIndexOutOfBoundsError)):
        _ = df.slice0([2, 4])

    with pytest.raises((IndexOutOfBoundsError, GroupIndexOutOfBoundsError)):
        _ = df.slice1([0, 2])


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[], y=[], z=[]),
        DataFrame(x=[], y=[]).group_by(),
        DataFrame(x=[]).group_by().group_by(),
    ],
)
def test_slice_rowless(df):
    df = DataFrame(x=[], y=[], z=[])

    actual = df.slice0([])
    assert actual == df

    actual = df.slice1([])
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[], y=[], z=[]),
        DataFrame(x=[], y=[]).group_by(),
        DataFrame(x=[]).group_by().group_by(),
    ],
)
def test_slice_rowless_out_of_bounds(df):
    df = DataFrame(x=[], y=[], z=[])

    with pytest.raises(IndexOutOfBoundsError):
        _ = df.slice0([0])

    with pytest.raises(IndexOutOfBoundsError):
        _ = df.slice1([1])
