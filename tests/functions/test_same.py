import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.exceptions import FunctionArgumentTypeError

from .._types import numeric_types


@pytest.mark.parametrize(
    "values",
    [
        [True, True],
        [-1, -1],
        ["aa", "aa"],
        [None, None],
    ],
)
def test_same(values):
    df = DataFrame(x=values)
    actual = df.mutate(x="same(x)")
    assert actual == actual


@pytest.mark.parametrize(
    "values",
    [
        [True, True, False],
        [-1, -1, 2],
        ["aa", "aa", "bb"],
        [None, None, 1],
        [None, None, None],
    ],
)
def test_same_group_by(values):
    df = DataFrame(a=[0, 0, 1], x=values)
    actual = df.group_by("a").summarize(x="same(x)")
    expected = DataFrame(a=[0, 1], x=values[1:])
    assert actual == expected


@pytest.mark.parametrize("values", [[0, 1], [0.0, 1.0], ["a", "b"], [1, None]])
def test_same_error(values):
    df = DataFrame(x=values)
    # BaseException because Polars eats the SameError and raises a PyO3 PanicException,
    # which does not inherit from Exception and is not part of the Polars API.
    with pytest.raises(BaseException):  # noqa: B017, PT011
        _ = df.mutate(x="same(x)")


@pytest.mark.parametrize("values", [[0, 1, 2], [0.0, 1.0, 2.0], ["a", "b", "c"], [1, None, 2]])
def test_same_error_group_by(values):
    df = DataFrame(a=[0, 0, 1], x=values)
    # BaseException because Polars eats the SameError and raises a PyO3 PanicException,
    # which does not inherit from Exception and is not part of the Polars API.
    with pytest.raises(BaseException):  # noqa: B017, PT011
        _ = df.group_by("a").summarize(x="same(x)")


@pytest.mark.parametrize("dtype", numeric_types)
def test_preserves_type(dtype):
    df = DataFrame(x=Array[dtype](1, 1, 1))
    actual = df.group_by().summarize(y="same(x)")
    assert actual[:, "y"].data_type == dtype


@pytest.mark.parametrize(
    ("literal", "actual_type"),
    [("42", DataType.Whole64), ("-42", DataType.Integer64), ("4.2", DataType.Float64)],
)
def test_same_rejects_literal(literal, actual_type):
    df = DataFrame(x=[1, 2, 3])
    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.group_by().summarize(y=f"same({literal})")
    assert exc_info.value == FunctionArgumentTypeError(
        "same", "argument", "array type", actual_type
    )
