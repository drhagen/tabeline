import pytest

from tabeline import DataTable


def test_summarize():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = table.group("x").summarize(size="n()", max_y="max(y)")
    expected = DataTable(x=[0, 1], size=[2, 2], max_y=[2, 4])
    assert actual == expected


def test_summarize_back_reference():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = table.group("x").summarize(max_y="max(y)", inverted="-max_y")
    expected = DataTable(x=[0, 1], max_y=[2, 4], inverted=[-2, -4])
    assert actual == expected


def test_summarize_original_and_back_reference():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 5])
    actual = table.group("x").summarize(max_y="max(y)", range="max_y-min(y)")
    expected = DataTable(x=[0, 1], max_y=[2, 5], range=[1, 2])
    assert actual == expected


def test_literal_in_summarize():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = table.group("x").summarize(new="1")
    expected = DataTable(x=[0, 1], new=[1, 1])
    assert actual == expected


def test_empty_summarize():
    table = DataTable(x=[0, 0, 1, 1], y=[1, 2, 3, 4])
    actual = table.group("x").summarize()
    expected = DataTable(x=[0, 1])
    assert actual == expected


def test_empty_summarize_on_two_groups():
    table = DataTable(x=[0, 0, 1, 1, 0], y=[1, 2, 2, 2, 2], z=[1, 2, 3, 4, 5])
    actual = table.group("x", "y").summarize()
    expected = DataTable(x=[0, 0, 1], y=[1, 2, 2])
    assert actual == expected


@pytest.mark.parametrize(
    "table",
    [
        DataTable().group(),
        DataTable().group().group(),
    ],
)
def test_summarize_empty(table):
    actual = table.summarize()
    expected = table.ungroup()
    assert actual == expected


@pytest.mark.parametrize(
    "table",
    [
        DataTable.columnless(height=6).group(),
        DataTable.columnless(height=6).group().group(),
    ],
)
def test_summarize_columnless(table):
    actual = table.summarize()
    expected = table.slice0([0]).ungroup()
    assert actual == expected


@pytest.mark.parametrize(
    "expressions",
    [
        {"a": "max(w)", "b": "min(x)"},
        {"a": "1", "b": "2"},
        {"a": "max(w)", "b": "a + 1"},
    ],
)
def test_summarize_rowless(expressions):
    table = DataTable(w=[], x=[], y=[], z=[])
    actual = table.group("x", "y").summarize(**expressions)
    expected = DataTable(x=[], y=[], a=[], b=[])
    assert actual == expected
