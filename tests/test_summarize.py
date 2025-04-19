import pytest

from tabeline import DataFrame


def test_summarize():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = df.group_by("x").summarize(size="n()", max_y="max(y)")
    expected = DataFrame(x=[0, 1], size=[2, 2], max_y=[2, 4])
    assert actual == expected


def test_summarize_back_reference():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = df.group_by("x").summarize(max_y="max(y)", inverted="-max_y")
    expected = DataFrame(x=[0, 1], max_y=[2, 4], inverted=[-2, -4])
    assert actual == expected


def test_summarize_original_and_back_reference():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 5])
    actual = df.group_by("x").summarize(max_y="max(y)", range="max_y-min(y)")
    expected = DataFrame(x=[0, 1], max_y=[2, 5], range=[1, 2])
    assert actual == expected


def test_literal_in_summarize():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = df.group_by("x").summarize(new="1")
    expected = DataFrame(x=[0, 1], new=[1, 1])
    assert actual == expected


def test_empty_summarize():
    df = DataFrame(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = df.group_by("x").summarize()
    expected = DataFrame(x=[0, 1])
    assert actual == expected


def test_empty_summarize_on_two_groups():
    df = DataFrame(x=[0, 0, 1, 1, 0], y=[1, 2, 2, 2, 2], z=[1, 2, 3, 4, 5])
    actual = df.group_by("x", "y").summarize()
    expected = DataFrame(x=[0, 0, 1], y=[1, 2, 2])
    assert actual == expected


@pytest.mark.parametrize(
    "df",
    [
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
    ],
)
def test_summarize_empty(df):
    actual = df.summarize()
    expected = df.ungroup()
    assert actual == expected


@pytest.mark.parametrize(
    "df",
    [
        DataFrame.columnless(height=6).group_by(),
        DataFrame.columnless(height=6).group_by().group_by(),
    ],
)
def test_summarize_columnless(df):
    actual = df.summarize()
    assert actual.height == 1
    assert actual.column_names == ()
    assert actual.group_levels == df.group_levels[:-1]


@pytest.mark.parametrize(
    "expressions",
    [
        {"a": "max(w)", "b": "min(x)"},
        {"a": "1", "b": "2"},
        {"a": "max(w)", "b": "a + 1"},
    ],
)
def test_summarize_rowless(expressions):
    df = DataFrame(w=[], x=[], y=[], z=[])
    actual = df.group_by("x", "y").summarize(**expressions)
    expected = DataFrame(x=[], y=[], a=[], b=[])
    assert actual == expected
