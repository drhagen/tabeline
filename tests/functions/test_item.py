import pytest

from tabeline import DataFrame
from tabeline.testing import assert_data_frames_equal


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1, 2, 3], 1),
        ([None, 2, 3], None),
        ([1], 1),
        ([None], None),
        (["a", "b", "c"], "a"),
    ],
)
def test_first(values, expected):
    df = DataFrame(x=[0, 0, 0][: len(values)], y=values)
    actual = df.group_by("x").summarize(y="first(y)")
    expected = DataFrame(x=[0], y=[expected])
    assert actual == expected


def test_first_broadcast():
    df = DataFrame(id=[1, 1, 1, 2, 2, 2], x=[10, 20, 30, 40, 50, 60])
    actual = df.group_by("id").mutate(x="first(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 2, 2, 2], x=[10, 10, 10, 40, 40, 40])
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1, 2, 3], 3),
        ([1, 2, None], None),
        ([1], 1),
        ([None], None),
        (["a", "b", "c"], "c"),
    ],
)
def test_last(values, expected):
    df = DataFrame(x=[0, 0, 0][: len(values)], y=values)
    actual = df.group_by("x").summarize(y="last(y)")
    expected = DataFrame(x=[0], y=[expected])
    assert actual == expected


def test_last_broadcast():
    df = DataFrame(id=[1, 1, 1, 2, 2, 2], x=[10, 20, 30, 40, 50, 60])
    actual = df.group_by("id").mutate(x="last(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 2, 2, 2], x=[30, 30, 30, 60, 60, 60])
    assert_data_frames_equal(actual, expected)
