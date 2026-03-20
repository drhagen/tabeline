import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.exceptions import NumericTypeNotSatisfiedError
from tabeline.testing import assert_data_frames_equal


@pytest.mark.parametrize(
    ("expression", "expected_value", "expected_dtype"),
    [
        ("-(2)", -2, DataType.Integer64),
        ("-(-2)", 2, DataType.Integer64),
        ("-(2.5)", -2.5, DataType.Float64),
    ],
)
def test_negative_literal(expression, expected_value, expected_dtype):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=Array[expected_dtype](expected_value))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_negative_rejects_non_numeric(values, expected_type):
    df = DataFrame(x=values)

    with pytest.raises(NumericTypeNotSatisfiedError) as exc_info:
        df.mutate(y="-x")

    assert exc_info.value == NumericTypeNotSatisfiedError("-_", expected_type)
