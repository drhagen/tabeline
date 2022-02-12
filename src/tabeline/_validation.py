__all__ = ["missing", "assert_legal_columns"]

from typing import Sequence

from tabeline.exceptions import DuplicateColumn, GroupColumn, NonexistentColumn

missing = object()


def assert_legal_columns(
    columns: Sequence[str],
    existing_columns: Sequence[str],
    illegal_group_columns: Sequence[str] = (),
) -> None:
    columns_set: set[str] = set()
    existing_columns_set = set(existing_columns)
    group_column_set = set(illegal_group_columns)
    for column in columns:
        if column in columns_set:
            raise DuplicateColumn(column)

        if column not in existing_columns_set:
            raise NonexistentColumn(column)

        if column in group_column_set:
            raise GroupColumn(column)
