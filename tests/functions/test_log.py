import math

from tabeline import DataFrame
from tabeline.testing import assert_data_frames_equal

absolute_tolerance = 1e-6


def test_log():
    df = DataFrame(x=[1.0, math.e, 1 / math.e, None])
    actual = df.mutate(x="log(x)")
    expected = DataFrame(x=[0.0, 1.0, -1.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_log2():
    df = DataFrame(x=[1.0, 2.0, 0.5, None])
    actual = df.mutate(x="log2(x)")
    expected = DataFrame(x=[0.0, 1.0, -1.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_log10():
    df = DataFrame(x=[1.0, 10.0, 0.1, None])
    actual = df.mutate(x="log10(x)")
    expected = DataFrame(x=[0.0, 1.0, -1.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)
