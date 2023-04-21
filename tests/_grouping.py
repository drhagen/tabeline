__all__ = ["apply_groups"]

from tabeline import DataFrame


def apply_groups(df: DataFrame, group_levels: tuple[tuple[str, ...], ...]) -> DataFrame:
    for group_level in group_levels:
        df = df.group_by(*group_level)
    return df
