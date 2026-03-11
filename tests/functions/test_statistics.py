import math

import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import FunctionArgumentCountError, FunctionArgumentTypeError
from tabeline.testing import assert_data_frames_equal

absolute_tolerance = 1e-6


def test_std():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="std(x)")
    expected = DataFrame(id=[1, 2], x=[math.sqrt(5 / 3), None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_std_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="std(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[math.sqrt(5 / 3)] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_var():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="var(x)")
    expected = DataFrame(id=[1, 2], x=[5 / 3, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_var_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="var(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[5 / 3] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_sum():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="sum(x)")
    expected = DataFrame(id=[1, 2], x=[10.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_sum_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="sum(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[10.0] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_mean():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="mean(x)")
    expected = DataFrame(id=[1, 2], x=[2.5, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_mean_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="mean(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[2.5] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_median():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="median(x)")
    expected = DataFrame(id=[1, 2], x=[2.5, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_median_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="median(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[2.5] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="quantile(x, 0.75)")
    expected = DataFrame(id=[1, 2], x=[3.25, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="quantile(x, 0.75)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[3.25] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile_zero():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="quantile(x, 0)")
    expected = DataFrame(id=[1, 2], x=[1.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile_one():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="quantile(x, 1)")
    expected = DataFrame(id=[1, 2], x=[4.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile_expression():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    actual = df.group_by("id").summarize(x="quantile(x, 0.25*3)")
    expected = DataFrame(id=[1, 2], x=[3.25, 7.25])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile_rejects_one_arg():
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="quantile(x)")

    assert exc_info.value == FunctionArgumentCountError("quantile", 2, 1)


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_quantile_rejects_non_numeric_argument(values, expected_type):
    df = DataFrame(x=values)

    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.mutate(y="quantile(x, 0.5)")

    assert exc_info.value == FunctionArgumentTypeError(
        "quantile", "argument", "numeric type", expected_type
    )


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_quantile_rejects_non_numeric_quantile(values, expected_type):
    df = DataFrame(x=[1, 2, 3], q=values)

    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.mutate(y="quantile(x, q)")

    assert exc_info.value == FunctionArgumentTypeError(
        "quantile", "quantile", "numeric type", expected_type
    )


@pytest.mark.parametrize("function", ["std", "var", "sum", "mean", "median"])
@pytest.mark.parametrize(
    ("literal", "actual_type"),
    [("42", DataType.Whole64), ("-42", DataType.Integer64), ("4.2", DataType.Float64)],
)
def test_statistic_rejects_literal(function, literal, actual_type):
    df = DataFrame(x=[1, 2, 3])
    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.group_by().summarize(y=f"{function}({literal})")
    assert exc_info.value == FunctionArgumentTypeError(
        function, "argument", "array type", actual_type
    )


@pytest.mark.parametrize(
    ("literal", "actual_type"),
    [("42", DataType.Whole64), ("-42", DataType.Integer64), ("4.2", DataType.Float64)],
)
def test_quantile_rejects_literal_argument(literal, actual_type):
    df = DataFrame(x=[1, 2, 3])
    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.group_by().summarize(y=f"quantile({literal}, 0.5)")
    assert exc_info.value == FunctionArgumentTypeError(
        "quantile", "argument", "array type", actual_type
    )
