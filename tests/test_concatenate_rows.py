import pytest

from tabeline import DataFrame, concatenate_rows
from tabeline.exceptions import UnmatchedColumnsError, UnmatchedGroupLevelsError


def test_concatenate_rows():
    df1 = DataFrame(x=[0, 1], y=["a", "b"])
    df2 = DataFrame(x=[3, 3], y=["c", "c"])
    actual = concatenate_rows(df1, df2)
    expected = DataFrame(x=[0, 1, 3, 3], y=["a", "b", "c", "c"])
    assert actual == expected


def test_concatenate_rows_grouped():
    df1 = DataFrame(x=[0, 1], y=["a", "b"]).group_by("x")
    df2 = DataFrame(x=[3, 3], y=["c", "c"]).group_by("x")
    actual = concatenate_rows(df1, df2)
    expected = DataFrame(x=[0, 1, 3, 3], y=["a", "b", "c", "c"]).group_by("x")
    assert actual == expected


def test_concatenate_rows_extra_columns():
    df1 = DataFrame(x=[0, 1], y=["a", "b"])
    df2 = DataFrame(x=[3, 3], y=["c", "c"], z=[True, False])
    with pytest.raises(UnmatchedColumnsError):
        _ = concatenate_rows(df1, df2)


def test_concatenate_rows_missing_columns():
    df1 = DataFrame(x=[0, 1], y=["a", "b"])
    df2 = DataFrame(x=[3, 3])
    with pytest.raises(UnmatchedColumnsError):
        _ = concatenate_rows(df1, df2)


def test_concatenate_rows_reordered_columns():
    df1 = DataFrame(x=[0, 1], y=["a", "b"])
    df2 = DataFrame(y=["c", "c"], x=[3, 3])
    with pytest.raises(UnmatchedColumnsError):
        _ = concatenate_rows(df1, df2)


def test_concatenate_rows_different_groups():
    df1 = DataFrame(x=[0, 1], y=["a", "b"]).group_by("x")
    df2 = DataFrame(x=[3, 3], y=["c", "c"]).group_by("y")
    with pytest.raises(UnmatchedGroupLevelsError):
        _ = concatenate_rows(df1, df2)


def test_concatenate_rows_single_data_frame():
    df = DataFrame(x=[0, 1], y=["a", "b"])
    actual = concatenate_rows(df)
    assert actual == df


def test_concatenate_rows_single_data_frame_grouped():
    df = DataFrame(x=[0, 1], y=["a", "b"]).group_by("x")
    actual = concatenate_rows(df)
    assert actual == df


def test_concatenate_rows_three_data_frames():
    df1 = DataFrame(x=[0, 1], y=["a", "b"])
    df2 = DataFrame(x=[3, 3], y=["c", "c"])
    df3 = DataFrame(x=[4, 1], y=["e", "b"])
    actual = concatenate_rows(df1, df2, df3)
    expected = DataFrame(x=[0, 1, 3, 3, 4, 1], y=["a", "b", "c", "c", "e", "b"])
    assert actual == expected
