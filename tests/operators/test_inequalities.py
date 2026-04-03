import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.exceptions import IncomparableTypesError
from tabeline.testing import assert_data_frames_equal

from .._types import numeric_types


@pytest.mark.parametrize("dtype_left", numeric_types)
@pytest.mark.parametrize("dtype_right", numeric_types)
@pytest.mark.parametrize(
    ("op", "results"),
    [
        ("<", [True, False, None, None, None]),
        (">", [False, False, None, None, None]),
        ("<=", [True, True, None, None, True]),
        (">=", [False, True, None, None, True]),
    ],
)
def test_numeric_inequalities(dtype_left, dtype_right, op, results):
    df = DataFrame(
        a=Array[dtype_left](2, 4, None, 3, None),
        b=Array[dtype_right](3, 4, 2, None, None),
    )
    actual = df.transmute(c=f"a {op} b")
    expected = DataFrame(c=results)
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("dtype", numeric_types)
@pytest.mark.parametrize("op", [">=", "<="])
def test_null_ge_le_nothing(dtype, op):
    df = DataFrame(a=Array[dtype](None, None), b=[None, None])
    expected = DataFrame(c=[True, True])

    actual = df.transmute(c=f"a {op} b")
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c=f"b {op} a")
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("dtype", numeric_types)
@pytest.mark.parametrize("op", [">", "<"])
def test_null_gt_lt_nothing(dtype, op):
    df = DataFrame(a=Array[dtype](None, None), b=[None, None])
    expected = DataFrame(c=[None, None])

    actual = df.transmute(c=f"a {op} b")
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c=f"b {op} a")
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("op", [">=", "<="])
@pytest.mark.parametrize("nulls", [[], [None, None]])
def test_nothing_ge_le_numeric(op, nulls):
    df = DataFrame(n=nulls, a=list(range(len(nulls))))
    expected = df.transmute(c="False")

    actual = df.transmute(c=f"n {op} a")
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c=f"a {op} n")
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("op", [">", "<"])
@pytest.mark.parametrize("nulls", [[], [None, None]])
def test_nothing_gt_lt_numeric(op, nulls):
    df = DataFrame(n=nulls, a=list(range(len(nulls))))
    expected = DataFrame(c=nulls)

    actual = df.transmute(c=f"n {op} a")
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c=f"a {op} n")
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("op", [">=", "<="])
@pytest.mark.parametrize("nulls", [[], [None, None]])
def test_nothing_ge_le_nothing(op, nulls):
    df = DataFrame(a=nulls, b=nulls)
    expected = df.transmute(c="True")

    actual = df.transmute(c=f"a {op} b")
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize("op", [">", "<"])
@pytest.mark.parametrize("nulls", [[], [None, None]])
def test_nothing_gt_lt_nothing(op, nulls):
    df = DataFrame(a=nulls, b=nulls)
    expected = DataFrame(c=nulls)

    actual = df.transmute(c=f"a {op} b")
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("expression", "operation"),
    [
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
def test_inequality_rejects_incomparable_types(
    expression, operation, left_values, right_values, left_type, right_type
):
    df = DataFrame(x=left_values, y=right_values)

    with pytest.raises(IncomparableTypesError) as exc_info:
        df.filter(expression)

    assert exc_info.value == IncomparableTypesError(operation, left_type, right_type)
