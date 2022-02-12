__all__ = ["apply_groups"]

from tabeline import DataTable


def apply_groups(table: DataTable, group_levels: tuple[tuple[str, ...], ...]) -> DataTable:
    for group_level in group_levels:
        table = table.group(*group_level)
    return table
