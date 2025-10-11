import pytest

from tabeline import DataFrame
from tabeline.testing import assert_data_frames_equal

relative_tolerance = 1e-12


def test_trapz():
    df = DataFrame(
        id=[0, 0, 0, 1, 1, 1],
        t=[2.0, 4.0, 5.0, 10.0, 11.0, 14.0],
        y=[0.0, 1.0, 1.0, 2.0, 3.0, None],
    )
    actual = df.group_by("id").summarize(q="trapz(t, y)")
    expected = DataFrame(id=[0, 1], q=[2.0, None])
    assert_data_frames_equal(actual, expected, relative_tolerance=relative_tolerance)


def test_trapz_integers():
    df = DataFrame(
        id=[0, 0, 0, 1, 1, 1],
        t=[2, 4, 5, 10, 11, 14],
        y=[0, 1, 1, 2, 3, None],
    )
    actual = df.group_by("id").summarize(q="trapz(t, y)")
    expected = DataFrame(id=[0, 1], q=[2.0, None])
    assert_data_frames_equal(actual, expected, relative_tolerance=relative_tolerance)


def test_trapz_not_sorted():
    df = DataFrame(id=[1, 1, 1], t=[2, 5, 4], y=[0, 1, 1])

    # BaseException because Polars eats the SameError and raises a PyO3 PanicException,
    # which does not inherit from Exception and is not part of the Polars API.
    with pytest.raises(BaseException):  # noqa: B017, PT011
        _ = df.group_by("id").summarize(y="trapz(t, y)")


def test_trapz_with_nulls():
    df = DataFrame(id=[1, 1, 1], t=[2, 3, None], y=[0, 1, 1])

    # BaseException because Polars eats the SameError and raises a PyO3 PanicException,
    # which does not inherit from Exception and is not part of the Polars API.
    with pytest.raises(BaseException):  # noqa: B017, PT011
        _ = df.group_by("id").summarize(y="trapz(t, y)")
