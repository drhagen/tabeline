import pytest

from tabeline import DataFrame, concatenate_columns
from tabeline.exceptions import DuplicateColumnError, HasGroupsError, UnmatchedHeightError


def test_concatenate_columns():
    df1 = DataFrame(x=[0, 1], y=["a", "b"])
    df2 = DataFrame(z=[True, False])
    actual = concatenate_columns(df1, df2)
    expected = DataFrame(x=[0, 1], y=["a", "b"], z=[True, False])
    assert actual == expected


def test_concatenate_columns_grouped():
    df1 = DataFrame(x=[0, 1], y=["a", "b"]).group_by("x")
    df2 = DataFrame(z=[True, False]).group_by("z")
    with pytest.raises(HasGroupsError):
        _ = concatenate_columns(df1, df2)


def test_concatenate_columns_single_data_frame_grouped():
    df = DataFrame(x=[0, 1], y=["a", "b"]).group_by("x")
    with pytest.raises(HasGroupsError):
        _ = concatenate_columns(df)


def test_concatenate_columns_later_only_data_frame_grouped():
    df1 = DataFrame(x=[0, 1], y=["a", "b"])
    df2 = DataFrame(z=[True, False]).group_by("z")
    with pytest.raises(HasGroupsError):
        _ = concatenate_columns(df1, df2)


def test_concatenate_columns_unmatched_height():
    df1 = DataFrame(x=[0, 1], y=["a", "b"])
    df2 = DataFrame(z=[True])
    with pytest.raises(UnmatchedHeightError):
        _ = concatenate_columns(df1, df2)


def test_concatenate_columns_duplicated_columns():
    df1 = DataFrame(x=[0, 1], y=["a", "b"])
    df2 = DataFrame(x=[True, False])
    with pytest.raises(DuplicateColumnError):
        _ = concatenate_columns(df1, df2)
