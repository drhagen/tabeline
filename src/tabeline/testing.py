from polars.testing import assert_frame_equal

from ._data_table import DataTable


def assert_table_equal(
    left: DataTable, right: DataTable, reltol: float = 0.0, abstol: float = 0.0
) -> None:
    assert left.shape == right.shape
    assert left.group_levels == right.group_levels
    assert_frame_equal(left._df, right._df, check_dtype=False, rtol=reltol, atol=abstol)
