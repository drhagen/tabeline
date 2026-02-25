import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import FunctionArgumentCountError, FunctionArgumentTypeError


@pytest.mark.parametrize(
    "function",
    [
        "sqrt",
        "exp",
        "abs",
        "log",
        "log2",
        "log10",
        "ceil",
        "floor",
        "sin",
        "cos",
        "tan",
        "arcsin",
        "arccos",
        "arctan",
        "is_finite",
        "is_nan",
        "is_null",
        "to_boolean",
        "to_float",
        "to_integer",
        "to_string",
        "first",
        "last",
        "any",
        "all",
        "same",
        "max",
        "min",
        "std",
        "var",
        "sum",
        "mean",
        "median",
    ],
)
def test_one_arg_function_rejects_zero_args(function):
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y=f"{function}()")

    error = exc_info.value
    assert error.function == function
    assert error.expected == 1
    assert error.actual == 0


@pytest.mark.parametrize(
    "function",
    [
        "sqrt",
        "exp",
        "abs",
        "log",
        "log2",
        "log10",
        "ceil",
        "floor",
        "sin",
        "cos",
        "tan",
        "arcsin",
        "arccos",
        "arctan",
        "is_finite",
        "is_nan",
        "is_null",
        "to_boolean",
        "to_float",
        "to_integer",
        "to_string",
        "first",
        "last",
        "any",
        "all",
        "same",
        "max",
        "min",
        "std",
        "var",
        "sum",
        "mean",
        "median",
    ],
)
def test_one_arg_function_rejects_two_args(function):
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y=f"{function}(x, x)")

    error = exc_info.value
    assert error.function == function
    assert error.expected == 1
    assert error.actual == 2


@pytest.mark.parametrize(
    "function",
    [
        "sqrt",
        "exp",
        "abs",
        "log",
        "log2",
        "log10",
        "ceil",
        "floor",
        "sin",
        "cos",
        "tan",
        "arcsin",
        "arccos",
        "arctan",
        "std",
        "var",
        "sum",
        "mean",
        "median",
    ],
)
@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_numeric_function_rejects_non_numeric(function, values, expected_type):
    df = DataFrame(x=values)

    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.mutate(y=f"{function}(x)")

    assert exc_info.value.function == function
    assert exc_info.value.actual == expected_type
