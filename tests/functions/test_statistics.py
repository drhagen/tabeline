import math

from tabeline import DataFrame
from tabeline.testing import assert_data_frames_equal

absolute_tolerance = 1e-6


def test_std():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="std(x)")
    expected = DataFrame(id=[1, 2], x=[math.sqrt(5 / 3), None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_std_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="std(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[math.sqrt(5 / 3)] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_var():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="var(x)")
    expected = DataFrame(id=[1, 2], x=[5 / 3, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_var_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="var(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[5 / 3] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_sum():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="sum(x)")
    expected = DataFrame(id=[1, 2], x=[10.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_sum_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="sum(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[10.0] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_mean():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="mean(x)")
    expected = DataFrame(id=[1, 2], x=[2.5, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_mean_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="mean(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[2.5] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_median():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="median(x)")
    expected = DataFrame(id=[1, 2], x=[2.5, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_median_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="median(x)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[2.5] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="quantile(x, 0.75)")
    expected = DataFrame(id=[1, 2], x=[3.25, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile_broadcast():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").mutate(x="quantile(x, 0.75)").ungroup()
    expected = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[3.25] * 4 + [None] * 3)
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile_zero():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="quantile(x, 0)")
    expected = DataFrame(id=[1, 2], x=[1.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile_one():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None])
    actual = df.group_by("id").summarize(x="quantile(x, 1)")
    expected = DataFrame(id=[1, 2], x=[4.0, None])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)


def test_quantile_expression():
    df = DataFrame(id=[1, 1, 1, 1, 2, 2, 2, 2], x=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    actual = df.group_by("id").summarize(x="quantile(x, 0.25*3)")
    expected = DataFrame(id=[1, 2], x=[3.25, 7.25])
    assert_data_frames_equal(actual, expected, absolute_tolerance=absolute_tolerance)
