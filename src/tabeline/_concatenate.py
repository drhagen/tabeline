__all__ = ["concatenate_rows", "concatenate_columns"]

import polars as pl

from tabeline._data_frame import DataFrame
from tabeline.exceptions import (
    DuplicateColumnError,
    HasGroupsError,
    UnmatchedColumnsError,
    UnmatchedGroupLevelsError,
    UnmatchedHeightError,
)


def concatenate_rows(df: DataFrame, *dfs: DataFrame) -> DataFrame:
    for df_i in dfs:
        if df_i.column_names != df.column_names:
            raise UnmatchedColumnsError(df.column_names, df_i.column_names)

        if df.group_levels != df_i.group_levels:
            raise UnmatchedGroupLevelsError(df.group_levels, df_i.group_levels)

    return DataFrame(
        pl.concat([df._df, *(df_i._df for df_i in dfs)], how="vertical"), df.group_levels
    )


def concatenate_columns(df: DataFrame, *dfs: DataFrame) -> DataFrame:
    if df.group_levels != ():
        raise HasGroupsError()

    found_columns = set(df.column_names)
    for df_i in dfs:
        if df_i.height != df.height:
            raise UnmatchedHeightError(df.height, df_i.height)

        if df_i.group_levels != ():
            raise HasGroupsError()

        for column in df_i.column_names:
            if column in found_columns:
                raise DuplicateColumnError(column)
        found_columns.update(df_i.column_names)

    return DataFrame(
        pl.concat([df._df, *(df_i._df for df_i in dfs)], how="horizontal"), df.group_levels
    )
