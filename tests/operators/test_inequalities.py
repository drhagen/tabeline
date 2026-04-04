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
        ("<=", [True, True, None, None, None]),
        (">=", [False, True, None, None, None]),
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
@pytest.mark.parametrize("op", [">", "<", ">=", "<="])
def test_null_inequality_nothing(dtype, op):
    df = DataFrame(a=Array[dtype](None, None), b=[None, None])
    expected = DataFrame(c=[None, None])

    actual = df.transmute(c=f"a {op} b")
    assert_data_frames_equal(actual, expected)

    actual = df.transmute(c=f"b {op} a")
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
