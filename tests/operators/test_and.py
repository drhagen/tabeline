import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import TypeMismatchError
from tabeline.testing import assert_data_frames_equal


def test_and():
    df = DataFrame(a=[True, True, False, False], b=[True, False, True, False])
    actual = df.transmute(c="a & b")
    expected = DataFrame(c=[True, False, False, False])
    assert_data_frames_equal(actual, expected)


def test_and_null_left():
    df = DataFrame(a=[None, None], b=[True, False])
    actual = df.transmute(c="a & b")
    expected = DataFrame(c=[None, False])
    assert_data_frames_equal(actual, expected)


def test_and_null_right():
    df = DataFrame(a=[True, False], b=[None, None])
    actual = df.transmute(c="a & b")
    expected = DataFrame(c=[None, False])
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("nulls", [[], [None, None]])
def test_and_both_null(nulls):
    df = DataFrame(a=nulls, b=nulls)
    actual = df.transmute(c="a & b")
    expected = DataFrame(c=nulls)
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        ([1, 2, 3], DataType.Integer64),
        (["a", "b", "c"], DataType.String),
    ],
)
def test_and_rejects_non_boolean_left_operand(values, expected_type):
    df = DataFrame(x=values, y=[True, False, True])

    with pytest.raises(TypeMismatchError) as exc_info:
        df.filter("x & y")

    assert exc_info.value == TypeMismatchError("and", DataType.Boolean, expected_type)


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        ([1, 2, 3], DataType.Integer64),
        (["a", "b", "c"], DataType.String),
    ],
)
def test_and_rejects_non_boolean_right_operand(values, expected_type):
    df = DataFrame(x=[True, False, True], y=values)

    with pytest.raises(TypeMismatchError) as exc_info:
        df.filter("x & y")

    assert exc_info.value == TypeMismatchError("and", DataType.Boolean, expected_type)
