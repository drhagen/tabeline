import pytest

try:
    from pandas import DataFrame
except ImportError:
    pytest.skip("Pandas not available", allow_module_level=True)

from tabeline import DataTable


@pytest.mark.parametrize(
    ["df", "table"],
    [
        [
            DataFrame(dict(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True])),
            DataTable(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True]),
        ],
        [
            DataFrame(),
            DataTable(),
        ],
        [
            DataFrame(index=range(6)),
            DataTable.columnless(height=6),
        ],
    ],
)
def test_pandas_conversion(df, table):
    assert table == DataTable.from_pandas(df)
    assert df.equals(table.to_pandas())


def test_pandas_conversion_rowless():
    # Polars and Pandas have no concept of List[Nothing]
    df = DataFrame(dict(x=[], y=[], z=[]))
    actual = DataTable.from_pandas(df)
    assert actual.shape == (0, 3)
    assert actual.column_names == ("x", "y", "z")

    table = DataTable(x=[], y=[], z=[])
    actual = table.to_pandas()
    assert actual.shape == (0, 3)
    assert tuple(actual.columns) == ("x", "y", "z")
