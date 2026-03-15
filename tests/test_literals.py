import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.testing import assert_data_frames_equal

from ._xfail import xfail_param

absolute_tolerance = 1e-6


def test_positive_integer_literal():
    df = DataFrame(x=[1, 2])
    actual = df.transmute(a="42")
    expected = DataFrame(a=Array[DataType.Whole64](42, 42))
    assert_data_frames_equal(actual, expected)


def test_negative_integer_literal():
    df = DataFrame(x=[1, 2])
    actual = df.transmute(a="-42")
    expected = DataFrame(a=Array[DataType.Integer64](-42, -42))
    assert_data_frames_equal(actual, expected)


def test_float_literal():
    df = DataFrame(x=[1, 2])
    actual = df.transmute(a="3.14")
    expected = DataFrame(a=Array[DataType.Float64](3.14, 3.14))
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_boolean_literal():
    df = DataFrame(x=[1, 2])
    actual = df.transmute(a="True")
    expected = DataFrame(a=Array[DataType.Boolean](True, True))
    assert_data_frames_equal(actual, expected)


def test_null_literal():
    df = DataFrame(x=[1, 2])
    actual = df.transmute(a="None")
    expected = DataFrame(a=Array[DataType.Nothing](None, None))
    assert_data_frames_equal(actual, expected)


@pytest.mark.parametrize(
    ("dtype", "literal", "expected_dtype"),
    [
        # Small literal fits in column type — no widening
        (DataType.Whole8, "0", DataType.Whole8),
        (DataType.Whole8, "255", DataType.Whole8),
        # Literal exceeds Whole8 (max 255) — widens to Whole16
        (DataType.Whole8, "256", DataType.Whole16),
        (DataType.Whole8, "65535", DataType.Whole16),
        # Literal exceeds Whole16 (max 65535) — widens to Whole32
        (DataType.Whole16, "65536", DataType.Whole32),
        (DataType.Whole16, "4294967295", DataType.Whole32),
        # Literal exceeds Whole32 (max ~4B) — widens to Whole64
        (DataType.Whole32, "4294967296", DataType.Whole64),
        # PyO3 passes integers in as i64, so this doesn't fit
        xfail_param(DataType.Whole32, "18446744073709551615", DataType.Whole64),
        # Negative literal with Whole type — signed + widened
        (DataType.Whole8, "-1", DataType.Integer8),
        (DataType.Whole8, "-128", DataType.Integer8),
        # Negative literal exceeds Integer8 (min -128) — widens to Integer16
        (DataType.Integer8, "-129", DataType.Integer16),
        (DataType.Integer8, "-32768", DataType.Integer16),
        # Negative literal exceeds Integer16 (min -32768) — widens to Integer32
        (DataType.Integer16, "-32769", DataType.Integer32),
        (DataType.Integer16, "-2147483648", DataType.Integer32),
        # Negative literal exceeds Integer32 (min ~-2B) — widens to Integer64
        (DataType.Integer32, "-2147483649", DataType.Integer64),
        # PyO3 passes integers in as i64, so this doesn't fit
        xfail_param(DataType.Integer32, "-9223372036854775808", DataType.Integer64),
    ],
)
def test_literal_widening(dtype, literal, expected_dtype):
    df = DataFrame(x=Array[dtype](1))
    actual = df.transmute(result=f"x + {literal}")
    assert actual[:, "result"].data_type == expected_dtype
