import math

from tabeline import DataFrame
from tabeline.testing import assert_data_frames_equal

absolute_tolerance = 1e-6


def test_sin():
    df = DataFrame(x=[0.0, 1.0, -math.pi, None])
    actual = df.mutate(x="sin(x)")
    expected = DataFrame(x=[0.0, math.sin(1.0), 0.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_cos():
    df = DataFrame(x=[0.0, 1.0, -math.pi, None])
    actual = df.mutate(x="cos(x)")
    expected = DataFrame(x=[1.0, math.cos(1.0), -1.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_tan():
    df = DataFrame(x=[0.0, 1.0, -math.pi, None])
    actual = df.mutate(x="tan(x)")
    expected = DataFrame(x=[0.0, math.tan(1.0), 0.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_arcsin():
    df = DataFrame(x=[0.0, 0.5, -1.0, None])
    actual = df.mutate(x="arcsin(x)")
    expected = DataFrame(x=[0.0, math.asin(0.5), -math.pi / 2, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_arccos():
    df = DataFrame(x=[1.0, 0.5, -1.0, None])
    actual = df.mutate(x="arccos(x)")
    expected = DataFrame(x=[0.0, math.acos(0.5), math.pi, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_arctan():
    df = DataFrame(x=[0.0, 1.0, -1.0, None])
    actual = df.mutate(x="arctan(x)")
    expected = DataFrame(x=[0.0, math.atan(1.0), -math.pi / 4, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)
