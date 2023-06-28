import pytest

import tabeline as tb

pd = pytest.importorskip("pandas")


@pytest.mark.parametrize(
    ("pandas_df", "df"),
    [
        (
            pd.DataFrame({"x": [0, 0, 1], "y": ["a", "b", "b"], "z": [True, False, True]}),
            tb.DataFrame(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True]),
        ),
        (
            pd.DataFrame(),
            tb.DataFrame(),
        ),
        (
            pd.DataFrame(index=range(6)),
            tb.DataFrame.columnless(height=6),
        ),
    ],
)
def test_pandas_conversion(pandas_df, df):
    assert df == tb.DataFrame.from_pandas(pandas_df)
    assert pandas_df.equals(df.to_pandas())


def test_pandas_conversion_rowless():
    # Polars and Pandas have no concept of List[Nothing]
    pandas_df = pd.DataFrame({"x": [], "y": [], "z": []})
    actual = tb.DataFrame.from_pandas(pandas_df)
    assert actual.shape == (0, 3)
    assert actual.column_names == ("x", "y", "z")

    df = tb.DataFrame(x=[], y=[], z=[])
    actual = df.to_pandas()
    assert actual.shape == (0, 3)
    assert tuple(actual.columns) == ("x", "y", "z")
