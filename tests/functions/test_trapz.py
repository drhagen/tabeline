import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import FunctionArgumentCountError, FunctionArgumentTypeError
from tabeline.testing import assert_data_frames_equal

relative_tolerance = 1e-12


def test_trapz():
    df = DataFrame(
        id=[0, 0, 0, 1, 1, 1],
        t=[2.0, 4.0, 5.0, 10.0, 11.0, 14.0],
        y=[0.0, 1.0, 1.0, 2.0, 3.0, None],
    )
    actual = df.group_by("id").summarize(q="trapz(t, y)")
    expected = DataFrame(id=[0, 1], q=[2.0, None])
    assert_data_frames_equal(actual, expected, relative_tolerance=relative_tolerance)


def test_trapz_integers():
    df = DataFrame(
        id=[0, 0, 0, 1, 1, 1],
        t=[2, 4, 5, 10, 11, 14],
        y=[0, 1, 1, 2, 3, None],
    )
    actual = df.group_by("id").summarize(q="trapz(t, y)")
    expected = DataFrame(id=[0, 1], q=[2.0, None])
    assert_data_frames_equal(actual, expected, relative_tolerance=relative_tolerance)


def test_trapz_not_sorted():
    df = DataFrame(id=[1, 1, 1], t=[2, 5, 4], y=[0, 1, 1])

    # BaseException because Polars eats the SameError and raises a PyO3 PanicException,
    # which does not inherit from Exception and is not part of the Polars API.
    with pytest.raises(BaseException):  # noqa: B017, PT011
        _ = df.group_by("id").summarize(y="trapz(t, y)")


def test_trapz_with_nulls():
    df = DataFrame(id=[1, 1, 1], t=[2, 3, None], y=[0, 1, 1])

    # BaseException because Polars eats the SameError and raises a PyO3 PanicException,
    # which does not inherit from Exception and is not part of the Polars API.
    with pytest.raises(BaseException):  # noqa: B017, PT011
        _ = df.group_by("id").summarize(y="trapz(t, y)")


def test_trapz_rejects_one_arg():
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="trapz(x)")

    assert exc_info.value == FunctionArgumentCountError("trapz", 2, 1)


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_trapz_rejects_non_numeric_independent_argument(values, expected_type):
    df = DataFrame(x=values, y=[1, 2, 3])

    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.mutate(z="trapz(x, y)")

    assert exc_info.value == FunctionArgumentTypeError("trapz", "t", "numeric type", expected_type)


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_trapz_rejects_non_numeric_dependent_argument(values, expected_type):
    df = DataFrame(x=[1, 2, 3], y=values)

    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.mutate(z="trapz(x, y)")

    assert exc_info.value == FunctionArgumentTypeError("trapz", "y", "numeric type", expected_type)


@pytest.mark.parametrize(
    ("literal", "actual_type"),
    [("42", DataType.Whole64), ("-42", DataType.Integer64), ("4.2", DataType.Float64)],
)
@pytest.mark.parametrize(
    ("expression_template", "parameter"),
    [
        ("trapz({literal}, y)", "t"),
        ("trapz(t, {literal})", "y"),
    ],
)
def test_trapz_rejects_literal(literal, actual_type, expression_template, parameter):
    df = DataFrame(t=[1, 2, 3], y=[1.0, 2.0, 3.0])
    expression = expression_template.format(literal=literal)
    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.group_by().summarize(q=expression)
    assert exc_info.value == FunctionArgumentTypeError(
        "trapz", parameter, "array type", actual_type
    )
