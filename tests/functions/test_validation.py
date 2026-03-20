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

    assert exc_info.value == FunctionArgumentCountError(function, 1, 0)


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

    assert exc_info.value == FunctionArgumentCountError(function, 1, 2)


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
        "max",
        "min",
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

    assert exc_info.value == FunctionArgumentTypeError(
        function, "argument", "numeric type", expected_type
    )
