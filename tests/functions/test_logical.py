import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.testing import assert_data_frames_equal


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([True, True, True], True),
        ([False, True, False], True),
        ([False, False, False], False),
        ([True, False, None], True),
        ([False, False, None], None),
        ([None, None, None], None),
    ],
)
def test_any(values, expected):
    df = DataFrame(x=[0, 0, 0], y=Array[DataType.Boolean](*values))
    actual = df.group_by("x").summarize(y="any(y)")
    expected = DataFrame(x=[0], y=Array[DataType.Boolean](expected))
    assert actual == expected


def test_any_broadcast():
    df = DataFrame(id=[1, 1, 1, 2, 2, 2], x=[True, False, True, False, False, None])
    actual = df.group_by("id").mutate(x="any(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 2, 2, 2], x=[True] * 3 + [None] * 3)
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([True, True, True], True),
        ([False, True, False], False),
        ([False, False, False], False),
        ([True, True, None], None),
        ([False, True, None], False),
        ([None, None, None], None),
    ],
)
def test_all(values, expected):
    df = DataFrame(x=[0, 0, 0], y=Array[DataType.Boolean](*values))
    actual = df.group_by("x").summarize(y="all(y)")
    expected = DataFrame(x=[0], y=Array[DataType.Boolean](expected))
    assert actual == expected


def test_all_broadcast():
    df = DataFrame(id=[1, 1, 1, 2, 2, 2], x=[True, True, False, True, True, None])
    actual = df.group_by("id").mutate(x="all(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 2, 2, 2], x=[False] * 3 + [None] * 3)
    assert_data_frames_equal(actual, expected)
