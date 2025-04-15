from typing import Any

import pytest

from tabeline import DataFrame
from tabeline.exceptions import GroupColumnError, NonexistentColumnError


def test_deselect():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = df.deselect("x", "z")
    expected = DataFrame(y=[True, False, True])
    assert actual == expected


full_columns = {
    "a": [1, 0, 1, 0],
    "b": ["a", "b", "b", "b"],
    "c": [True, True, True, False],
    "d": [3.4, 2.7, -9.0, 0.0],
}

empty_columns = {
    "a": [],
    "b": [],
    "c": [],
    "d": [],
}


@pytest.mark.parametrize("test_columns", [full_columns, empty_columns])
@pytest.mark.parametrize(
    ("input_columns", "deselectors", "expected_columns"),
    [
        ([], [], []),
        (["a"], [], ["a"]),
        (["a", "b"], ["a"], ["b"]),
        (["a", "b", "c"], ["a", "c"], ["b"]),
        (["a", "b", "c"], ["c", "a"], ["b"]),
        (["a", "b", "c"], ["b", "c", "a"], []),
        (["a", "b", "c", "d"], ["c", "a"], ["b", "d"]),
    ],
)
def test_deselect_columns(
    input_columns: list[str],
    deselectors: list[str],
    expected_columns: list[str],
    test_columns: dict[str, Any],
):
    df = DataFrame(**{name: test_columns[name] for name in input_columns})
    actual = df.deselect(*deselectors)
    if len(expected_columns) == 0:
        expected = DataFrame.columnless(height=df.height)
    else:
        expected = DataFrame(**{name: test_columns[name] for name in expected_columns})
    assert actual == expected


def test_deselect_nonexistent_column():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])

    with pytest.raises(NonexistentColumnError):
        _ = df.deselect("x", "a")


def test_deselect_group_column():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x")

    with pytest.raises(GroupColumnError):
        _ = df.deselect("x")


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_deselect_empty(df):
    actual = df.deselect()
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame.columnless(height=6),
        DataFrame.columnless(height=6).group_by(),
        DataFrame.columnless(height=6).group_by().group_by(),
    ],
)
def test_deselect_columnless(df):
    actual = df.deselect()
    assert actual == df
