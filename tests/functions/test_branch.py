import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import (
    FunctionArgumentCountError,
    FunctionArgumentTypeError,
    IncompatibleTypesError,
    SummarizeTypeError,
)


def test_if_else():
    df = DataFrame(id=[0, 0, 0, 1, 1, 1], x=[2, 4, 5, 10, 11, -1], y=[0, -2, 1, 2, 3, 4])
    actual = df.transmute(id="id", q="if_else(id == 1, x, y)")
    expected = DataFrame(id=[0, 0, 0, 1, 1, 1], q=[0, -2, 1, 10, 11, -1])
    assert actual == expected


def test_if_else_no_otherwise():
    df = DataFrame(id=[0, 0, 0, 1, 1, 1], x=[2, 4, 5, 10, 11, -1])
    actual = df.transmute(id="id", q="if_else(id == 1, x)")
    expected = DataFrame(id=[0, 0, 0, 1, 1, 1], q=[None, None, None, 10, 11, -1])
    assert actual == expected


def test_if_else_grouped():
    df = DataFrame(id=[0, 0, 0, 1, 1, 1], x=[2, 5, 5, 10, 11, -13])
    actual = df.group_by("id").transmute(x="if_else(x == max(x), x, 0)")
    expected = DataFrame(id=[0, 0, 0, 1, 1, 1], x=[0, 5, 5, 0, 11, 0]).group_by("id")
    assert actual == expected


def test_if_else_grouped_no_otherwise():
    df = DataFrame(id=[0, 0, 0, 1, 1, 1], x=[2, 5, 5, 10, 11, -13])
    actual = df.group_by("id").transmute(x="if_else(x == max(x), x)")
    expected = DataFrame(id=[0, 0, 0, 1, 1, 1], x=[None, 5, 5, None, 11, None]).group_by("id")
    assert actual == expected


@pytest.mark.parametrize("default", ["", ", a"])
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(a=[]),
        DataFrame(a=[]).group_by(),
        DataFrame(a=[]).group_by().group_by(),
        DataFrame(a=[]).group_by("a"),
        DataFrame(a=[], b=[], c=[]).group_by("a", "b"),
        DataFrame(a=[], b=[], c=[]).group_by("a").group_by("b"),
    ],
)
def test_if_else_on_rowless_data_frame_with_mutate(default, df):
    actual = df.mutate(x=f"if_else(a!=0, a{default})")
    expected = df.mutate(x="1")
    assert actual == expected


def test_if_else_rejects_one_arg():
    df = DataFrame(x=[True, False, True])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="if_else(x)")

    assert exc_info.value == FunctionArgumentCountError("if_else", 2, 1)


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        ([1, 2, 3], DataType.Integer64),
        (["a", "b", "c"], DataType.String),
    ],
)
def test_if_else_condition_must_be_boolean(values, expected_type):
    df = DataFrame(x=values, y=[4, 5, 6])

    with pytest.raises(FunctionArgumentTypeError) as exc_info:
        df.mutate(z="if_else(x, y, 0)")

    assert exc_info.value == FunctionArgumentTypeError(
        "if_else", "condition", "Boolean or Nothing", expected_type
    )


def test_if_else_rejects_incompatible_branch_types():
    df = DataFrame(x=[True, False, True])

    with pytest.raises(IncompatibleTypesError) as exc_info:
        df.mutate(y="if_else(x, 1, 'hello')")

    assert exc_info.value == IncompatibleTypesError(
        "if_else", DataType.Integer64, DataType.String
    )


def test_if_else_broadcasts_on_array_condition():
    df = DataFrame(x=[1, 1, 2, 2], y=[10, 20, 30, 40])

    with pytest.raises(SummarizeTypeError):
        df.group_by("x").summarize(z="if_else(y > 15, 1, 0)")
