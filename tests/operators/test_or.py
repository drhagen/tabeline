import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import TypeMismatchError
from tabeline.testing import assert_data_frames_equal


def test_or():
    df = DataFrame(a=[True, True, False, False], b=[True, False, True, False])
    actual = df.transmute(c="a | b")
    expected = DataFrame(c=[True, True, True, False])
    assert_data_frames_equal(actual, expected)


def test_or_null_left():
    df = DataFrame(a=[None, None], b=[True, False])
    actual = df.transmute(c="a | b")
    expected = DataFrame(c=[True, None])
    assert_data_frames_equal(actual, expected)


def test_or_null_right():
    df = DataFrame(a=[True, False], b=[None, None])
    actual = df.transmute(c="a | b")
    expected = DataFrame(c=[True, None])
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("nulls", [[], [None, None]])
def test_or_both_null(nulls):
    df = DataFrame(a=nulls, b=nulls)
    actual = df.transmute(c="a | b")
    expected = DataFrame(c=nulls)
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        ([1, 2, 3], DataType.Integer64),
        (["a", "b", "c"], DataType.String),
    ],
)
def test_or_rejects_non_boolean_left_operand(values, expected_type):
    df = DataFrame(x=values, y=[True, False, True])

    with pytest.raises(TypeMismatchError) as exc_info:
        df.filter("x | y")

    assert exc_info.value == TypeMismatchError("or", DataType.Boolean, expected_type)


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        ([1, 2, 3], DataType.Integer64),
        (["a", "b", "c"], DataType.String),
    ],
)
def test_or_rejects_non_boolean_right_operand(values, expected_type):
    df = DataFrame(x=[True, False, True], y=values)

    with pytest.raises(TypeMismatchError) as exc_info:
        df.filter("x | y")

    assert exc_info.value == TypeMismatchError("or", DataType.Boolean, expected_type)
