from tabeline import Array, DataFrame, DataType
from tabeline.testing import assert_data_frames_equal

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
