import pytest

from tabeline import DataFrame
from tabeline.exceptions import DuplicateColumnError, NonexistentColumnError


def test_select():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    actual = df.select("x", "z")
    expected = DataFrame(x=[0, 0, 1], z=["a", "b", "c"])
    assert actual == expected


test_columns = {
    "a": [1, 0, 1, 0],
    "b": ["a", "b", "b", "b"],
    "c": [True, True, True, False],
    "d": [3.4, 2.7, -9.0, 0.0],
}


@pytest.mark.parametrize(
    ("input_columns", "selectors"),
    [
        (["a", "b", "c"], ["a"]),
        (["a", "b", "c"], ["b"]),
        (["a", "b", "c"], ["c"]),
        (["a", "b", "c", "d"], ["b", "c"]),
        (["a", "b", "c", "d"], ["c", "b"]),
        (["a", "b", "c", "d"], ["a", "b", "c", "d"]),
        (["a", "b", "c", "d"], ["d", "b", "a", "c"]),
    ],
)
def test_select_columns(input_columns: list[str], selectors: list[str]):
    df = DataFrame(**{name: test_columns[name] for name in input_columns})
    actual = df.select(*selectors)
    expected = DataFrame(**{name: test_columns[name] for name in selectors})
    assert actual == expected


@pytest.mark.parametrize(
    "input_columns",
    [
        [],
        ["a"],
        ["a", "b"],
    ],
)
def test_select_no_columns(input_columns):
    df = DataFrame(**{name: test_columns[name] for name in input_columns})
    actual = df.select()
    expected = DataFrame.columnless(height=df.height)
    assert actual == expected


@pytest.mark.parametrize(
    ("input_columns", "groups", "selectors", "expected_columns"),
    [
        ([], [], [], []),
        (["a"], [["a"]], [], ["a"]),
        (["a", "b"], [["a", "b"]], [], ["a", "b"]),
        (["a", "b"], [["a"], ["b"]], [], ["a", "b"]),
        (["a"], [["a"]], ["a"], ["a"]),
        (["a", "b"], [["a", "b"]], ["b"], ["a", "b"]),
        (["a", "b"], [["a"], ["b"]], ["b"], ["a", "b"]),
        (["a", "b"], [["a", "b"]], ["a"], ["b", "a"]),
        (["a", "b"], [["a"], ["b"]], ["a"], ["b", "a"]),
        (["a", "b", "c", "d"], [["a", "b"]], ["c"], ["a", "b", "c"]),
        (["a", "b", "c", "d"], [["a", "b"]], ["a", "c"], ["b", "a", "c"]),
        (["a", "b", "c", "d"], [["a", "b"]], ["a", "b", "c"], ["a", "b", "c"]),
        (["a", "b", "c", "d"], [["b", "a"]], ["c"], ["a", "b", "c"]),
        (["a", "b", "c", "d"], [["b", "a"]], ["a", "c"], ["b", "a", "c"]),
        (["a", "b", "c", "d"], [["b", "a"]], ["b", "c"], ["a", "b", "c"]),
        (["a", "b", "c", "d"], [["b", "a"]], ["a", "b", "c"], ["a", "b", "c"]),
        (["a", "b", "c", "d"], [["b", "a"], []], ["a", "b", "c"], ["a", "b", "c"]),
        (["a", "b", "c", "d"], [["b"], ["a"]], ["a", "b", "c"], ["a", "b", "c"]),
        (["a", "b", "c", "d"], [[], ["b", "a"]], ["a", "b", "c"], ["a", "b", "c"]),
    ],
)
def test_select_columns_grouped(
    input_columns: list[str],
    groups: list[list[str]],
    selectors: list[str],
    expected_columns: list[str],
):
    df = DataFrame(**{name: test_columns[name] for name in input_columns})
    for level in groups:
        df = df.group_by(*level)
    actual = df.select(*selectors)
    expected = DataFrame(**{name: test_columns[name] for name in expected_columns})
    for level in groups:
        expected = expected.group_by(*level)
    assert actual == expected


def test_select_nonexistent_column():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])

    with pytest.raises(NonexistentColumnError):
        _ = df.select("x", "a")


def test_select_duplicate_columns():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])

    with pytest.raises(DuplicateColumnError):
        _ = df.select("x", "x")


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_select_empty(df):
    actual = df.select()
    assert actual == df


@pytest.mark.parametrize(
    "df",
    [
        DataFrame.columnless(height=6),
        DataFrame.columnless(height=6).group_by(),
        DataFrame.columnless(height=6).group_by().group_by(),
    ],
)
def test_select_columnless(df):
    actual = df.select()
    assert actual == df
