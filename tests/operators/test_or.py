import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import TypeMismatchError


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

    error = exc_info.value
    assert error.operation == "or"
    assert error.expected == DataType.Boolean
    assert error.actual == expected_type


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

    error = exc_info.value
    assert error.operation == "or"
    assert error.expected == DataType.Boolean
    assert error.actual == expected_type
