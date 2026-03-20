import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import IncomparableTypesError, NumericTypeNotSatisfiedError


@pytest.mark.parametrize(
    ("expression", "operation"),
    [
        ("x + y", "addition"),
        ("x - y", "subtraction"),
        ("x * y", "multiplication"),
        ("x / y", "division"),
        ("x // y", "floor division"),
        ("x % y", "modulo"),
        ("x ** y", "exponentiation"),
    ],
)
@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_arithmetic_rejects_non_numeric_operand(expression, operation, values, expected_type):
    df = DataFrame(x=[1, 2, 3], y=values)

    with pytest.raises(NumericTypeNotSatisfiedError) as exc_info:
        df.mutate(z=expression)

    assert exc_info.value == NumericTypeNotSatisfiedError(operation, expected_type)


@pytest.mark.parametrize(
    ("expression", "operation"),
    [
        ("x == y", "equality"),
        ("x != y", "inequality"),
        ("x > y", "greater than"),
        ("x >= y", "greater than or equal"),
        ("x < y", "less than"),
        ("x <= y", "less than or equal"),
    ],
)
@pytest.mark.parametrize(
    ("left_values", "right_values", "left_type", "right_type"),
    [
        ([1, 2, 3], ["a", "b", "c"], DataType.Integer64, DataType.String),
        ([1, 2, 3], [True, False, True], DataType.Integer64, DataType.Boolean),
        (["a", "b", "c"], [True, False, True], DataType.String, DataType.Boolean),
    ],
)
def test_comparison_rejects_incomparable_types(
    expression, operation, left_values, right_values, left_type, right_type
):
    df = DataFrame(x=left_values, y=right_values)

    with pytest.raises(IncomparableTypesError) as exc_info:
        df.filter(expression)

    assert exc_info.value == IncomparableTypesError(operation, left_type, right_type)
