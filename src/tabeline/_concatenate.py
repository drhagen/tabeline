__all__ = ["concatenate_rows"]

import polars as pl

from tabeline._data_frame import DataFrame
from tabeline.exceptions import UnmatchedColumns, UnmatchedGroupLevels


def concatenate_rows(df: DataFrame, *dfs: DataFrame) -> DataFrame:
    for df_i in dfs:
        if df_i.column_names != df.column_names:
            raise UnmatchedColumns(df.column_names, df_i.column_names)

        if df.group_levels != df_i.group_levels:
            raise UnmatchedGroupLevels(df.group_levels, df_i.group_levels)

    return DataFrame(
        pl.concat([df._df, *(df_i._df for df_i in dfs)], how="vertical"), df.group_levels
    )
