import math

import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.exceptions import FunctionArgumentTypeError

from .._types import float_data_types, integer_data_types, whole_data_types


def test_max():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    actual = df.group_by("id").summarize(x="max(x)")
    expected = DataFrame(id=[1, 2], x=[4.0, 7.0])
    assert actual == expected


def test_max_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    actual = df.group_by("id").mutate(x="max(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[4.0] * 4 + [7.0] * 3)
    assert actual == expected


def test_max_with_nulls():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="max(x)")
    expected = DataFrame(id=[1, 2], x=[4.0, 6.0])
    assert actual == expected


def test_max_with_all_nulls():
    df = DataFrame(id=[1, 1, 1], x=[None, None, None])
    actual = df.group_by("id").summarize(x="max(x)")
    expected = DataFrame(id=[1], x=[None])
    assert actual == expected


def test_max_with_negative_numbers():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[-1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0])
    actual = df.group_by("id").summarize(x="max(x)")
    expected = DataFrame(id=[1, 2], x=[-1.0, -5.0])
    assert actual == expected


def test_max_with_integers():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1, 2, 3, 4, 5, 6, 7])
    actual = df.group_by("id").summarize(x="max(x)")
    expected = DataFrame(id=[1, 2], x=[4, 7])
    assert actual == expected


def test_max_with_infinity():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, math.inf, 3.0, 4.0, 5.0, 6.0, 7.0])
    actual = df.group_by("id").summarize(x="max(x)")
    expected = DataFrame(id=[1, 2], x=[math.inf, 7.0])
    assert actual == expected


def test_max_single_value():
    df = DataFrame(id=[1], x=[42.0])
    actual = df.group_by("id").summarize(x="max(x)")
    expected = DataFrame(id=[1], x=[42.0])
    assert actual == expected


def test_min():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    actual = df.group_by("id").summarize(x="min(x)")
    expected = DataFrame(id=[1, 2], x=[1.0, 5.0])
    assert actual == expected


def test_min_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    actual = df.group_by("id").mutate(x="min(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0] * 4 + [5.0] * 3)
    assert actual == expected


def test_min_with_nulls():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="min(x)")
    expected = DataFrame(id=[1, 2], x=[1.0, 5.0])
    assert actual == expected


def test_min_with_all_nulls():
    df = DataFrame(id=[1, 1, 1], x=[None, None, None])
    actual = df.group_by("id").summarize(x="min(x)")
    expected = DataFrame(id=[1], x=[None])
    assert actual == expected


def test_min_with_negative_numbers():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[-1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0])
    actual = df.group_by("id").summarize(x="min(x)")
    expected = DataFrame(id=[1, 2], x=[-4.0, -7.0])
    assert actual == expected


def test_min_with_integers():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1, 2, 3, 4, 5, 6, 7])
    actual = df.group_by("id").summarize(x="min(x)")
    expected = DataFrame(id=[1, 2], x=[1, 5])
    assert actual == expected


def test_min_with_infinity():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, -math.inf, 3.0, 4.0, 5.0, 6.0, 7.0])
    actual = df.group_by("id").summarize(x="min(x)")
    expected = DataFrame(id=[1, 2], x=[-math.inf, 5.0])
    assert actual == expected


def test_min_single_value():
    df = DataFrame(id=[1], x=[42.0])
    actual = df.group_by("id").summarize(x="min(x)")
    expected = DataFrame(id=[1], x=[42.0])
    assert actual == expected


def test_max_min_combined():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    actual = df.group_by("id").summarize(min_x="min(x)", max_x="max(x)")
    expected = DataFrame(id=[1, 2], min_x=[1.0, 5.0], max_x=[4.0, 7.0])
    assert actual == expected


@pytest.mark.parametrize("function", ["max", "min"])
@pytest.mark.parametrize("dtype", whole_data_types + integer_data_types + float_data_types)
def test_reduction_extrema_preserves_type(function, dtype):
    df = DataFrame(x=Array[dtype](1, 3, 2))
    actual = df.group_by().summarize(a=f"{function}(x)")
    assert actual[:, "a"].data_type == dtype


@pytest.mark.parametrize("function", ["max", "min"])
@pytest.mark.parametrize(
    ("literal", "actual_type"),
    [("42", DataType.Whole64), ("-42", DataType.Integer64), ("4.2", DataType.Float64)],
)
def test_reduction_extrema_rejects_literal(function, literal, actual_type):
    df = DataFrame(x=[1, 2, 3])
    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.group_by().summarize(y=f"{function}({literal})")
    assert exc_info.value == FunctionArgumentTypeError(
        function, "argument", "array type", actual_type
    )
