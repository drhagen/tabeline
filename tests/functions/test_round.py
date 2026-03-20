import pytest

from tabeline import Array, DataFrame, DataType

from .._types import numeric_types


def test_floor():
    values = [1.2, 2.7, -1.8, None]
    expected = [1.0, 2.0, -2.0, None]
    df = DataFrame(x=values)
    actual = df.mutate(x="floor(x)")
    assert actual == DataFrame(x=expected)


def test_ceil():
    values = [1.2, 2.7, -1.8, None]
    expected = [2.0, 3.0, -1.0, None]
    df = DataFrame(x=values)
    actual = df.mutate(x="ceil(x)")
    assert actual == DataFrame(x=expected)


@pytest.mark.parametrize("dtype", numeric_types)
@pytest.mark.parametrize("expression", ["floor(x)", "ceil(x)"])
def test_preserves_type(expression, dtype):
    df = DataFrame(x=Array[dtype](1, 2, 3))
    actual = df.mutate(y=expression)
    assert actual[:, "y"].data_type == dtype


@pytest.mark.parametrize(
    ("expression", "expected_value", "expected_dtype"),
    [
        ("floor(2)", 2, DataType.Whole64),
        ("floor(-3)", -3, DataType.Integer64),
        ("floor(3.7)", 3.0, DataType.Float64),
        ("floor(-3.7)", -4.0, DataType.Float64),
        ("ceil(2)", 2, DataType.Whole64),
        ("ceil(-3)", -3, DataType.Integer64),
        ("ceil(3.7)", 4.0, DataType.Float64),
        ("ceil(-3.7)", -3.0, DataType.Float64),
    ],
)
def test_round_literal(expression, expected_value, expected_dtype):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    assert actual == DataFrame(result=[expected_value])
    assert actual[:, "result"].data_type == expected_dtype
