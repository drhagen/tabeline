import polars as pl
import pytest
from polars.testing import assert_frame_equal

import tabeline as tb


@pytest.mark.parametrize(
    ["polars_df", "df"],
    [
        [
            pl.DataFrame(dict(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True])),
            tb.DataFrame(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True]),
        ],
        [
            pl.DataFrame(dict(x=[], y=[], z=[])),
            tb.DataFrame(x=[], y=[], z=[]),
        ],
        [
            pl.DataFrame(),
            tb.DataFrame(),
        ],
    ],
)
def test_polars_conversion(polars_df, df):
    assert df == tb.DataFrame.from_polars(polars_df)
    assert_frame_equal(polars_df, df.to_polars())


def test_to_polars_columnless():
    df = tb.DataFrame.columnless(height=6)
    actual = df.to_polars()
    expected = pl.DataFrame()
    assert_frame_equal(actual, expected)
