from math import inf, nan

import pytest

from tabeline import Array, DataFrame, DataType
from tabeline.testing import assert_data_frames_equal

relative_tolerance = 1e-12


@pytest.mark.parametrize(
    ("ys", "t", "expected"),
    [
        # Actual interpolation
        ([0.3, 0.1, 0.8], 2.5, 0.2),
        ([0.3, 0.1, None], 2.5, 0.2),
        ([0.3, 0.1, nan], 2.5, 0.2),
        ([0.3, 0.1, inf], 2.5, 0.2),
        ([0.3, 0.1, -nan], 2.5, 0.2),
        ([None, 0.1, 0.8], 2.5, None),
        ([0.3, None, 0.8], 2.5, None),
        ([nan, 0.1, 0.8], 2.5, nan),
        ([0.3, nan, 0.8], 2.5, nan),
        ([inf, 0.1, 0.8], 2.5, inf),
        ([0.3, inf, 0.8], 2.5, inf),
        ([-inf, 0.1, 0.8], 2.5, -inf),
        ([0.3, -inf, 0.8], 2.5, -inf),
        # First value equal
        ([0.3, 0.1, 0.8], 2.0, 0.3),
        ([None, 0.1, 0.8], 2.0, None),
        ([nan, 0.1, 0.8], 2.0, nan),
        ([inf, 0.1, 0.8], 2.0, inf),
        ([-inf, 0.1, 0.8], 2.0, -inf),
        # Middle value equal
        ([0.3, 0.1, 0.8], 3.0, 0.1),
        ([0.3, None, 0.8], 3.0, None),
        ([0.3, nan, 0.8], 3.0, nan),
        ([0.3, inf, 0.8], 3.0, inf),
        ([0.3, -inf, 0.8], 3.0, -inf),
        # Last value equal
        ([0.3, 0.1, 0.8], 5.0, 0.8),
        ([0.3, 0.1, None], 5.0, None),
        ([0.3, 0.1, nan], 5.0, nan),
        ([0.3, 0.1, inf], 5.0, inf),
        ([0.3, 0.1, -inf], 5.0, -inf),
        # Outside bounds
        ([0.3, 0.1, 0.8], 1.0, None),
        ([0.3, 0.1, 0.8], 6.0, None),
    ],
)
def test_interp(ys, t, expected):
    df = DataFrame(
        id=[1, 1, 1],
        ts=[2.0, 3.0, 5.0],
        ys=ys,
    )
    actual = df.group_by("id").summarize(y=f"interp({t}, ts, ys)")
    expected_df = DataFrame(id=[1], y=Array[DataType.Float64](expected))
    assert_data_frames_equal(actual, expected_df, relative_tolerance=relative_tolerance)


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(id=[1, 1, 1], ts=[2, 3, 5], ys=[3.0, 0.0, 8.0]),
        DataFrame(id=[1, 1, 1], ts=[2.0, 3.0, 5.0], ys=[3, 0, 8]),
        DataFrame(id=[1, 1, 1], ts=[2, 3, 5], ys=[3, 0, 8]),
    ],
)
def test_interp_integers(df):
    actual = df.group_by("id").summarize(y="interp(2.5, ts, ys)")
    expected_df = DataFrame(id=[1], y=[1.5])
    assert_data_frames_equal(actual, expected_df, relative_tolerance=relative_tolerance)


@pytest.mark.skip("Not implemented")
def test_interp_float32():
    df = DataFrame(
        id=[1, 1, 1],
        ts=Array[DataType.Float32](2.0, 3.0, 5.0),
        ys=Array[DataType.Float32](0.3, 0.1, 0.8),
    )
    actual = df.group_by("id").summarize(y="interp(2.5, ts, ys)")
    expected_df = DataFrame(id=[1], y=Array[DataType.Float32](0.2))
    assert_data_frames_equal(actual, expected_df, relative_tolerance=relative_tolerance)


def test_interp_not_sorted():
    df = DataFrame(
        id=[1, 1, 1],
        ts=[3.0, 2.0, 5.0],
        ys=[0.1, 0.3, 0.8],
    )
    # BaseException because Polars eats the SameError and raises a PyO3 PanicException,
    # which does not inherit from Exception and is not part of the Polars API.
    with pytest.raises(BaseException):  # noqa: B017, PT011
        _ = df.group_by("id").summarize(y="interp(2.5, ts, ys)")


def test_interp_with_nulls():
    df = DataFrame(
        id=[1, 1, 1],
        ts=[2.0, None, 5.0],
        ys=[0.1, 0.3, 0.8],
    )
    # BaseException because Polars eats the SameError and raises a PyO3 PanicException,
    # which does not inherit from Exception and is not part of the Polars API.
    with pytest.raises(BaseException):  # noqa: B017, PT011
        _ = df.group_by("id").summarize(y="interp(2.5, ts, ys)")
