import pytest

import tabeline as tb

pl = pytest.importorskip("polars")
import polars.testing  # noqa: E402


@pytest.mark.parametrize("elements", [[], [0], [0, 1, 2], [True, False, True], ["a", "b", "c"]])
def test_array_conversion(elements):
    expected = tb.Array(*elements)

    series = pl.Series(values=elements)
    assert expected == tb.Array.from_polars(series)
    polars.testing.assert_series_equal(series, expected.to_polars())


@pytest.mark.parametrize(
    ("polars_df", "df"),
    [
        (
            pl.DataFrame({"x": [0, 0, 1], "y": ["a", "b", "b"], "z": [True, False, True]}),
            tb.DataFrame(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True]),
        ),
        (
            pl.DataFrame({"x": [], "y": [], "z": []}),
            tb.DataFrame(x=[], y=[], z=[]),
        ),
        (
            pl.DataFrame(),
            tb.DataFrame(),
        ),
    ],
)
def test_polars_conversion(polars_df, df):
    assert df == tb.DataFrame.from_polars(polars_df)
    polars.testing.assert_frame_equal(polars_df, df.to_polars())


def test_to_polars_columnless():
    # Polars has not concept of columnless data frames
    df = tb.DataFrame.columnless(height=6)
    actual = df.to_polars()
    expected = pl.DataFrame()
    polars.testing.assert_frame_equal(actual, expected)
