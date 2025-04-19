import math

from tabeline import DataFrame
from tabeline.testing import assert_data_frames_equal

absolute_tolerance = 1e-6


def test_sqrt():
    df = DataFrame(x=[0.0, 4.0, 6.25, None])
    actual = df.mutate(x="sqrt(x)")
    expected = DataFrame(x=[0.0, 2.0, 2.5, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_exp():
    df = DataFrame(x=[0.0, 1.0, 2.5, None])
    actual = df.mutate(x="exp(x)")
    expected = DataFrame(x=[1.0, math.e, math.exp(2.5), None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_pow():
    df = DataFrame(x=[2.0, 2.0, 4.0, None], y=[2.0, -2.0, 0.5, 3.0])
    actual = df.transmute(z="pow(x, y)")
    expected = DataFrame(z=[4.0, 0.25, 2.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)
