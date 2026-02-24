import pytest

from tabeline import DataFrame


def test_unknown_variable_error():
    from tabeline.exceptions import UnknownVariableError

    df = DataFrame(x=[1, 2, 3])

    # Try to filter with a non-existent variable
    with pytest.raises(UnknownVariableError) as exc_info:
        df.filter("y > 0")

    error = exc_info.value
    # Check that attributes are accessible
    assert error.name == "y"
    assert "x" in error.available
    assert len(error.available) >= 1

    # Check error message
    error_msg = str(error)
    assert "Unknown variable 'y'" in error_msg
    assert "x" in error_msg


def test_type_mismatch_error():
    from tabeline import DataType
    from tabeline.exceptions import TypeMismatchError

    df = DataFrame(x=[1, 2, 3])

    # Try to use NOT on a non-boolean
    with pytest.raises(TypeMismatchError) as exc_info:
        df.filter("~x")

    error = exc_info.value
    # Check that attributes are accessible
    assert error.operation == "~_"
    assert error.expected == DataType.Boolean
    assert error.actual == DataType.Integer64

    # Check error message
    error_msg = str(error)
    assert "Expected Boolean" in error_msg
    assert "~_" in error_msg
    assert "Integer64" in error_msg


def test_incomparable_types_error():
    from tabeline import DataType
    from tabeline.exceptions import IncomparableTypesError

    df = DataFrame(x=[1, 2, 3], y=["a", "b", "c"])

    # Try to compare incompatible types
    with pytest.raises(IncomparableTypesError) as exc_info:
        df.filter("x == y")

    error = exc_info.value
    # Check that attributes are accessible
    assert error.left_type == DataType.Integer64
    assert error.right_type == DataType.String

    # Check error message
    error_msg = str(error)
    assert "Cannot compare" in error_msg
    assert "Integer64" in error_msg
    assert "String" in error_msg


def test_type_requirement_not_satisfied_error():
    from tabeline import DataType
    from tabeline.exceptions import NumericTypeNotSatisfiedError

    df = DataFrame(x=["a", "b", "c"])

    # Try to use positive operator on a string
    with pytest.raises(NumericTypeNotSatisfiedError) as exc_info:
        df.mutate(y="+x")

    error = exc_info.value
    # Check that attributes are accessible
    assert error.actual == DataType.String
    assert error.operation == "+_"

    # Check error message
    error_msg = str(error)
    assert "Expected numeric type" in error_msg
    assert "+_" in error_msg
    assert "String" in error_msg


def test_incompatible_types_error():
    from tabeline import DataType
    from tabeline.exceptions import NumericTypeNotSatisfiedError

    df = DataFrame(x=[1, 2, 3], y=["a", "b", "c"])

    # Try to add a string to an integer (string is not numeric)
    with pytest.raises(NumericTypeNotSatisfiedError) as exc_info:
        df.mutate(z="x + y")

    error = exc_info.value
    # Check that attributes are accessible
    assert error.operation == "addition"
    assert error.actual == DataType.String

    # Check error message
    error_msg = str(error)
    assert "Expected numeric type" in error_msg
    assert "addition" in error_msg
    assert "String" in error_msg
