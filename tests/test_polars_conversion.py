import pytest
from polars import DataFrame
from polars.testing import assert_frame_equal

from tabeline import DataTable


@pytest.mark.parametrize(
    ["df", "table"],
    [
        [
            DataFrame(dict(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True])),
            DataTable(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True]),
        ],
        [
            DataFrame(dict(x=[], y=[], z=[])),
            DataTable(x=[], y=[], z=[]),
        ],
        [
            DataFrame(),
            DataTable(),
        ],
    ],
)
def test_polars_conversion(df, table):
    assert table == DataTable.from_polars(df)
    assert_frame_equal(df, table.to_polars())


def test_to_polars_columnless():
    table = DataTable.columnless(height=6)
    actual = table.to_polars()
    expected = DataFrame()
    assert_frame_equal(actual, expected)
