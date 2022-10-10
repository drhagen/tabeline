from __future__ import annotations

__all__ = ["DataTable"]

from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Optional, Sequence, Union

import polars as pl

from ._dummy import dummy_name, dummy_table
from ._expression import substitute, to_polars
from ._expression.ast import Expression
from ._validation import assert_legal_columns, missing
from .exceptions import (
    GroupColumn,
    HasGroups,
    IndexOutOfRange,
    NoGroups,
    NonexistentColumn,
    RenameExisting,
)

# Singleton indicating that the default value is to error
error = object()

if TYPE_CHECKING:
    import pandas as pd


class DataTable:
    def __init__(
        self,
        polars_df: pl.DataFrame = missing,
        group_levels: tuple[tuple[str, ...], ...] = (),
        height: Optional[int] = None,
        /,
        **columns,
    ):
        self.groups: tuple[tuple[str, ...], ...]

        if polars_df is missing:
            self._df = pl.DataFrame(columns)
            self.group_levels = ()
            self.height = self._df.height  # With no columns, height is assumed to be 0
        elif len(columns) == 0:
            self._df = polars_df
            self.group_levels = group_levels
            if height is not None:
                self.height = height
            else:
                self.height = self._df.height  # With no height, height is taken from polars
        else:
            raise TypeError("DataTable() takes 0 positional arguments but 1 was given")

    @staticmethod
    def columnless(*, height: int) -> DataTable:
        return DataTable(pl.DataFrame({}), (), height)

    @property
    def width(self) -> int:
        return self._df.width

    @property
    def shape(self) -> tuple[int, int]:
        return self.height, self.width

    @property
    def column_names(self) -> tuple[str, ...]:
        return tuple(self._df.columns)

    @property
    def group_names(self) -> tuple[str, ...]:
        return tuple(names for level in self.group_levels for names in level)

    @staticmethod
    def from_dict(columns: dict[str, list[Any]], /) -> DataTable:
        df = pl.DataFrame(columns)
        return DataTable(df)

    @staticmethod
    def from_pandas(df: pd.DataFrame) -> DataTable:
        if df.shape[1] == 0:
            # Polars does not understand columnless tables
            return DataTable.columnless(height=df.shape[0])

        return DataTable(pl.from_pandas(df))

    def to_pandas(self) -> pd.DataFrame:
        import numpy as np
        import pandas as pd

        if len(self.group_levels) != 0:
            raise HasGroups()

        if self.width == 0:
            # Polars does not understand columnless tables
            return pd.DataFrame(np.empty((self.height, 0)))

        return self._df.to_pandas()

    @staticmethod
    def from_polars(df: pl.DataFrame) -> DataTable:
        return DataTable(df)

    def to_polars(self) -> pl.DataFrame:
        if len(self.group_levels) != 0:
            raise HasGroups()

        return self._df

    @staticmethod
    def read_csv(path: Path) -> DataTable:
        df = pl.read_csv(str(path))
        return DataTable(df)

    def write_csv(self, path: Path) -> None:
        if len(self.group_levels) != 0:
            raise HasGroups()

        self._df.write_csv(str(path))

    def slice0(self, indexes: list[int], /) -> DataTable:
        # Negative indexes are not supported by Polars, so they are not
        # supported in Tabeline.
        if self.width == 0:
            for index in indexes:
                if index >= self.height or index < 0:
                    raise IndexOutOfRange(index, self.height)
            return DataTable(self._df, self.group_levels, len(indexes))
        else:
            group_names = self.group_names
            if len(group_names) == 0:
                # Polars chokes on empty groups
                return DataTable(self._df.select(pl.all().take(indexes)), self.group_levels)
            else:
                # There is no easy way to slice by groups in Polars. Using
                # `take` on a group causes the sliced columns to be a column of
                # lists that must be exploded at the end. The exploding results
                # in clustering, so getting back the original row order requires
                # tagging each row with an index and sorting the result by that.
                # https://stackoverflow.com/q/71373783/
                group_set = set(self.group_names)
                non_group_columns = [
                    column for column in self.column_names if column not in group_set
                ] + ["_index"]

                if len(indexes) == 1:
                    # Polars is not type stable, so explode must be excluded
                    # when taking only one element
                    new_df = (
                        self._df.lazy()
                        .with_column(pl.arange(0, pl.count()).alias("_index"))
                        .groupby(list(group_names), maintain_order=True)
                        .agg(pl.all().take(indexes))
                        .sort("_index")
                        .drop("_index")
                        .collect()
                    )
                else:
                    new_df = (
                        self._df.lazy()
                        .with_column(pl.arange(0, pl.count()).alias("_index"))
                        .groupby(list(group_names), maintain_order=True)
                        .agg(pl.all().take(indexes))
                        .explode(non_group_columns)
                        .sort("_index")
                        .drop("_index")
                        .collect()
                    )

                return DataTable(new_df, self.group_levels)

    def slice1(self, indexes: list[int], /) -> DataTable:
        return self.slice0([index - 1 for index in indexes])

    def filter(self, predicate: str, /) -> DataTable:
        expression = to_polars(Expression.parse(predicate).or_die())

        if self.width == 0:
            # There is no way to evaluate an expression outside a datatable, so
            # make a dummy table with the right number of rows.
            # eager=True needed because lazy expressions are not allowed in
            # the constructor
            # https://github.com/pola-rs/polars/issues/2983
            height = dummy_table(self.height).filter(expression).height
            return DataTable(pl.DataFrame({}), self.group_levels, height)
        else:
            flat_groups = list(self.group_names)
            if len(flat_groups) > 0 and self.height > 0:
                windowed_expression = expression.over(flat_groups)
            else:
                # Polars chokes on an empty window
                # Polars chokes on window over rowless table
                windowed_expression = expression

            return DataTable(self._df.filter(windowed_expression), self.group_levels)

    def distinct(self, *columns: str) -> DataTable:
        assert_legal_columns(columns, self.column_names)

        # Polars chokes on duplicate columns
        group_set = set(self.group_names)
        unmentioned_columns = tuple(column for column in columns if column not in group_set)
        all_columns = list(self.group_names + unmentioned_columns)
        if len(all_columns) == 0:
            if self.height == 0:
                # Polars chokes on an empty distinct subset
                return self
            else:
                return DataTable(self._df.head(1), self.group_levels, 1)
        else:
            return DataTable(self._df.unique(subset=all_columns), self.group_levels)

    def unique(self) -> DataTable:
        if self.width == 0:
            return DataTable(pl.DataFrame({}), self.group_levels, min(1, self.height))

        return DataTable(self._df.unique(), self.group_levels)

    def cluster(self, *columns: str) -> DataTable:
        assert_legal_columns(columns, self.column_names, self.group_names)

        flat_groups = self.group_names

        all_columns = list(self.group_names + columns)

        if len(all_columns) == 0:
            # Polars chokes on empty window columns
            return self

        if len(flat_groups) == 0:
            # Polars chokes on empty window columns
            return DataTable(
                self._df.lazy()
                .with_column(pl.arange(0, pl.count()).alias("_index"))
                .with_column(pl.min("_index").over(all_columns))
                .select(pl.all().sort_by(["_index"]))
                .drop("_index")
                .collect(),
                self.group_levels,
                self.height,
            )
        else:
            return DataTable(
                self._df.lazy()
                .with_column(pl.arange(0, pl.count()).alias("_index"))
                .with_column(pl.min("_index").over(all_columns))
                .select(pl.all().sort_by(["_index"]).over(list(self.group_names)))
                .drop("_index")
                .collect(),
                self.group_levels,
                self.height,
            )

    def sort(self, *columns: str) -> DataTable:
        assert_legal_columns(columns, self.column_names, self.group_names)

        flat_groups = self.group_names
        if len(flat_groups) == 0 or self.height == 0:
            # Polars chokes on empty groups
            # Polars chokes on windowing over empty rows
            return DataTable(self._df.sort(list(columns)), self.group_levels, self.height)
        else:
            return DataTable(
                self._df.select(pl.all().sort_by(list(columns)).over(list(flat_groups))),
                self.group_levels,
                self.height,
            )

    def select(self, *columns: str) -> DataTable:
        assert_legal_columns(columns, self.column_names)

        # Group columns cannot be deselected. Prepend any group columns that
        # were not explicitly selected so that group columns can be reordered
        # by select, but not lost. Unmentioned group columns are retained in
        # their original order.
        select_set = set(columns)
        group_set = set(self.group_names)
        unmentioned_groups = tuple(
            column
            for column in self.column_names
            if column in group_set and column not in select_set
        )

        return DataTable(
            self._df.select(unmentioned_groups + columns), self.group_levels, self.height
        )

    def deselect(self, *columns: str) -> DataTable:
        assert_legal_columns(columns, self.column_names, self.group_names)

        return DataTable(self._df.drop(list(columns)), self.group_levels, self.height)

    def rename(self, **names: str) -> DataTable:
        # Renames are processed simultaneously. Overwriting an existing column
        # is not permitted with this operation. Temporary column names may not
        # be used; columns to be swapped should simply be swapped. Renaming a
        # group column is legal.
        # Note that in dplyr, the order is new_name=old_name and in polars
        # old_name=new_name.
        # Sometime in the 0.13.x series, Polars switched from sequential to
        # parallel. dplyr has always been sequential.

        columns_set = set(self.column_names)

        for old_column in names.values():
            if old_column not in columns_set:
                raise NonexistentColumn(old_column)
            else:
                columns_set.remove(old_column)

        for new_column in names.keys():
            if new_column in columns_set:
                raise RenameExisting(names[new_column], new_column)
            else:
                columns_set.add(new_column)

        rename_map = {old: new for new, old in names.items()}

        groups = tuple(
            tuple(rename_map.get(column, column) for column in level)
            for level in self.group_levels
        )

        return DataTable(self._df.rename(rename_map), groups, self.height)

    def mutate(self, **mutators: str) -> DataTable:
        group_set = set(self.group_names)
        for column in mutators.keys():
            if column in group_set:
                raise GroupColumn(column)

        if self.width == 0:
            df = dummy_table(self.height)
        else:
            df = self._df

        # Both mutate and transmute must compute each column individually
        # because a column may refer to previous columns, which is not allowed
        # in a select context in polars:
        # https://stackoverflow.com/q/71105136/
        polars_operation = df.lazy()
        if len(group_set) == 0:
            for name, mutator in mutators.items():
                polars_operation = polars_operation.with_column(
                    to_polars(Expression.parse(mutator).or_die()).alias(name)
                )
        else:
            for name, mutator in mutators.items():
                polars_operation = polars_operation.with_column(
                    to_polars(Expression.parse(mutator).or_die())
                    .over(list(self.group_names))
                    .alias(name)
                )

        if self.width == 0:
            polars_operation = polars_operation.drop(dummy_name)

        return DataTable(polars_operation.collect(), self.group_levels, self.height)

    def transmute(self, **mutators: str) -> DataTable:
        mutated_table = self.mutate(**mutators)

        # Keep group columns and explicitly mentioned columns, all in the order
        # of group columns followed by explicit columns
        return mutated_table.select(*self.group_names, *mutators.keys())

    def group(
        self, *columns: str, order: Literal["original", "cluster", "sort"] = "original"
    ) -> DataTable:
        assert_legal_columns(columns, self.column_names, self.group_names)

        if order == "original":
            ordered_table = self
        elif order == "cluster":
            ordered_table = self.cluster(*columns)
        elif order == "sort":
            ordered_table = self.sort(*columns)
        else:
            raise TypeError(
                f"For order, expected 'original', 'cluster', or 'sort', but got {order!r}"
            )

        return DataTable(ordered_table._df, self.group_levels + (columns,), self.height)

    def ungroup(self) -> DataTable:
        if len(self.group_levels) == 0:
            raise NoGroups()
        else:
            return DataTable(self._df, self.group_levels[:-1], self.height)

    def summarize(self, **reducers: str) -> DataTable:
        if len(self.group_levels) == 0:
            raise NoGroups()

        # There is no way to sequentially evaluate expressions in a groupby
        # context, so each reducer must be substituted into subsequent reducers:
        # https://stackoverflow.com/q/71120396/
        substituted_reducers = {}
        for name, reducer in reducers.items():
            substituted_reducers[name] = substitute(
                Expression.parse(reducer).or_die(), substituted_reducers
            )

        polars_expressions = [
            to_polars(reducer).alias(name) for name, reducer in substituted_reducers.items()
        ]

        if len(polars_expressions) == 0:
            # Polars chokes on empty agg. This is equivalent to dropping
            # everything but the group columns and then running distinct.
            return self.select().distinct().ungroup()
        else:
            if self.width == 0:
                df = dummy_table(self.height)
            else:
                df = self._df

            summarized = df.groupby(list(self.group_names), maintain_order=True).agg(
                polars_expressions
            )

            return DataTable(summarized, self.group_levels[:-1])

    def spread(self, key: str, value: str, *, fill: Any = error) -> DataTable:
        if len(self.group_levels) == 0:
            raise NoGroups()

        assert_legal_columns([key, value], self.column_names, self.group_names)

        df = self._df.pivot(index=list(self.group_names), columns=key, values=value)

        return DataTable(df, self.group_levels[:-1])

    def gather(self, key: str, value: str, *columns: str) -> DataTable:
        column_set = set(columns)
        all_columns = [column for column in self.column_names if column not in column_set]

        df = self._df.melt(
            id_vars=all_columns, value_vars=list(columns), variable_name=key, value_name=value
        )

        return DataTable(df, self.group_levels).group(key)

    def _resolve_join_by(
        self,
        by: Optional[Sequence[Union[str, tuple[str, str]]]],
        right_column_names: Sequence[str],
    ) -> tuple[Optional[list[str]], Optional[list[str]]]:
        if by is not None:
            left_key_columns = []
            right_key_columns = []
            for by_i in by:
                if isinstance(by_i, str):
                    left_key_columns.append(by_i)
                    right_key_columns.append(by_i)
                else:
                    left_key_column, right_key_column = by_i
                    left_key_columns.append(left_key_column)
                    right_key_columns.append(right_key_column)

            assert_legal_columns(left_key_columns, self.column_names)
            assert_legal_columns(right_key_columns, right_column_names)
        else:
            right_columns_set = set(right_column_names)
            common_columns = [
                column for column in self.column_names if column in right_columns_set
            ]

            left_key_columns = common_columns
            right_key_columns = common_columns

        return left_key_columns, right_key_columns

    def inner_join(
        self,
        other: DataTable,
        /,
        *,
        by: Optional[Sequence[Union[str, tuple[str, str]]]] = None,
    ) -> DataTable:
        if len(self.group_levels) != 0 or len(other.group_levels) != 0:
            raise NotImplementedError("Joins using grouped tables is not currently implemented")

        left_key_columns, right_key_columns = self._resolve_join_by(by, other.column_names)

        joined_df = (
            # Polars does not order the output, so sort by original orders
            self._df.lazy()
            .with_column(pl.arange(0, pl.count()).alias("_index1"))
            .join(
                other._df.lazy().with_column(pl.arange(0, pl.count()).alias("_index2")),
                left_on=left_key_columns,
                right_on=right_key_columns,
                how="inner",
            )
            .sort(["_index1", "_index2"])
            .drop(["_index1", "_index2"])
            .collect()
        )

        return DataTable(joined_df)

    def left_join(
        self,
        other: DataTable,
        /,
        *,
        by: Optional[Sequence[Union[str, tuple[str, str]]]] = None,
    ) -> DataTable:
        if len(self.group_levels) != 0 or len(other.group_levels) != 0:
            raise NotImplementedError("Joins using grouped tables is not currently implemented")

        left_key_columns, right_key_columns = self._resolve_join_by(by, other.column_names)

        joined_df = (
            # Polars does not order the output, so sort by original orders
            self._df.lazy()
            .with_column(pl.arange(0, pl.count()).alias("_index1"))
            .join(
                other._df.lazy().with_column(pl.arange(0, pl.count()).alias("_index2")),
                left_on=left_key_columns,
                right_on=right_key_columns,
                how="left",
            )
            .sort(["_index1", "_index2"])
            .drop(["_index1", "_index2"])
            .collect()
        )
        return DataTable(
            joined_df,
        )

    def outer_join(
        self,
        other: DataTable,
        /,
        *,
        by: Optional[Sequence[Union[str, tuple[str, str]]]] = None,
    ) -> DataTable:
        if len(self.group_levels) != 0 or len(other.group_levels) != 0:
            raise NotImplementedError("Joins using grouped tables is not currently implemented")

        left_key_columns, right_key_columns = self._resolve_join_by(by, other.column_names)

        joined_df = (
            # Polars does not order the output, so sort by original orders
            self._df.lazy()
            .with_column(pl.arange(0, pl.count()).alias("_index1"))
            .join(
                other._df.lazy().with_column(pl.arange(0, pl.count()).alias("_index2")),
                left_on=left_key_columns,
                right_on=right_key_columns,
                how="outer",
            )
            .sort(["_index1", "_index2"])
            .drop(["_index1", "_index2"])
            .collect()
        )
        return DataTable(
            joined_df,
        )

    def __eq__(self, other):
        if isinstance(other, DataTable):
            if self.group_levels != other.group_levels:
                return False

            if self.width == 0:
                # Polars does not understand columnless tables
                return self.height == other.height

            if self.height == 0:
                # Empty columns with different types are not equal in Polars,
                # but are in Tabeline.
                return self.column_names == other.column_names

            return self._df.frame_equal(other._df)

        return NotImplemented

    def __repr__(self):
        column_strs = [f"{name} = {list(values)!r}" for name, values in self._df.to_dict().items()]
        group_strs = [f".group({', '.join(map(repr, level))})" for level in self.group_levels]
        return f"DataTable({', '.join(column_strs)}){''.join(group_strs)}"

    def __str__(self):
        if len(self.group_levels) == 0:
            return str(self._df)
        else:
            groups_str = ",".join("[" + ",".join(level) + "]" for level in self.group_levels)
            return f"group levels: {groups_str}\n{self._df}"
