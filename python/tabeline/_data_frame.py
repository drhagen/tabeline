from __future__ import annotations

__all__ = ["DataFrame"]

from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

from ._array import Array, Element
from ._expression import parse_expression, to_py_expression
from ._record import Record
from ._tabeline import PyArray, PyDataFrame, PyExpression
from .exceptions import IncompatibleLengthError

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl


def py_data_frame_from_dict(columns: dict[str, Sequence[Element]]) -> PyDataFrame:
    cleaned_columns: list[tuple[str, PyArray]] = []
    height: int | None = None
    for name, elements in columns.items():
        match elements:
            case Array():
                array = elements._py_array
            case _:
                array = Array.from_sequence(elements)._py_array

        if height is None:
            height = len(array)
        elif len(array) != height:
            raise IncompatibleLengthError(height, len(array), name)

        cleaned_columns.append((name, array))

    if height is None:
        # Default height when no columns are provided
        height = 0

    return PyDataFrame.from_tuple_list(cleaned_columns, height)


def tuple_list_from_kwargs(columns: dict[str, str]) -> list[tuple[str, PyExpression]]:
    tuple_list = []
    for name, expression in columns.items():
        parsed_expression = parse_expression(expression)
        py_expression = to_py_expression(parsed_expression)
        tuple_list.append((name, py_expression))

    return tuple_list


def standardize_join_by(
    left: DataFrame, right: DataFrame, by: Sequence[str | tuple[str, str]] | None
) -> list[tuple[str, str]]:
    if by is None:
        left_names = left.column_names
        right_names = set(right.column_names)
        return [(name, name) for name in left_names if name in right_names]
    else:
        return [(name, name) if isinstance(name, str) else name for name in by]


class DataFrame:
    def __init__(
        self,
        py_data_frame: PyDataFrame = None,
        /,
        **columns: list[bool] | list[int] | list[float] | list[str],
    ):
        if isinstance(py_data_frame, PyDataFrame):
            if len(columns) != 0:
                raise TypeError(
                    "Passing a PyDataFrame is the private constructor, "
                    "which requires exactly one argument"
                )
            rust_data_frame = py_data_frame
        else:
            if py_data_frame is not None:
                raise TypeError("DataFrame() takes 0 positional arguments but 1 was given")
            rust_data_frame = py_data_frame_from_dict(columns)

        self._py_data_frame = rust_data_frame

    @staticmethod
    def columnless(height: int) -> DataFrame:
        return DataFrame(PyDataFrame.from_tuple_list([], height))

    @staticmethod
    def from_dict(columns: dict[str, Sequence[Element]]) -> DataFrame:
        return DataFrame(py_data_frame_from_dict(columns))

    def to_dict(self) -> dict[str, Array]:
        return {name: Array(py_array) for name, py_array in self._py_data_frame.to_tuple_list()}

    @property
    def height(self) -> int:
        return self._py_data_frame.height

    @property
    def width(self) -> int:
        return self._py_data_frame.width

    @property
    def shape(self) -> tuple[int, int]:
        return self.height, self.width

    @property
    def column_names(self) -> tuple[str]:
        return self._py_data_frame.column_names

    @property
    def group_levels(self) -> tuple[tuple[str, ...], ...]:
        return self._py_data_frame.group_levels

    def slice0(self, indexes: list[int]) -> DataFrame:
        return DataFrame(self._py_data_frame.slice0(indexes))

    def slice1(self, indexes: list[int]) -> DataFrame:
        return DataFrame(self._py_data_frame.slice1(indexes))

    def filter(self, predicate: str, /) -> DataFrame:
        expression = parse_expression(predicate)
        py_expression = to_py_expression(expression)
        return DataFrame(self._py_data_frame.filter(py_expression))

    def distinct(self, *columns: str) -> DataFrame:
        return DataFrame(self._py_data_frame.distinct(columns))

    def unique(self) -> DataFrame:
        return DataFrame(self._py_data_frame.unique())

    def sort(self, *columns: str) -> DataFrame:
        return DataFrame(self._py_data_frame.sort(columns))

    def cluster(self, *columns: str) -> DataFrame:
        return DataFrame(self._py_data_frame.cluster(columns))

    def select(self, *columns: str) -> DataFrame:
        return DataFrame(self._py_data_frame.select(columns))

    def deselect(self, *columns: str) -> DataFrame:
        return DataFrame(self._py_data_frame.deselect(columns))

    def rename(self, **columns: str) -> DataFrame:
        return DataFrame(self._py_data_frame.rename(list(columns.items())))

    def mutate(self, **columns: str) -> DataFrame:
        return DataFrame(self._py_data_frame.mutate(tuple_list_from_kwargs(columns)))

    def transmute(self, **columns: str) -> DataFrame:
        return DataFrame(self._py_data_frame.transmute(tuple_list_from_kwargs(columns)))

    def group_by(
        self, *columns: str, order: Literal["original", "cluster", "sort"] = "original"
    ) -> DataFrame:
        if order == "original":
            ordered_df = self
        elif order == "cluster":
            ordered_df = self.cluster(*columns)
        elif order == "sort":
            ordered_df = self.sort(*columns)
        else:
            raise TypeError(
                f"For order, expected 'original', 'cluster', or 'sort', but got {order!r}"
            )

        return DataFrame(ordered_df._py_data_frame.group_by(columns))

    def ungroup(self) -> DataFrame:
        return DataFrame(self._py_data_frame.ungroup())

    def summarize(self, **columns: str) -> DataFrame:
        return DataFrame(self._py_data_frame.summarize(tuple_list_from_kwargs(columns)))

    def spread(self, key: str, value: str) -> DataFrame:
        return DataFrame(self._py_data_frame.spread(key, value))

    def gather(self, key: str, value: str, *columns: str) -> DataFrame:
        return DataFrame(self._py_data_frame.gather(key, value, columns))

    def inner_join(
        self, other: DataFrame, by: Sequence[str | tuple[str, str]] | None = None
    ) -> DataFrame:
        return DataFrame(
            self._py_data_frame.inner_join(
                other._py_data_frame, standardize_join_by(self, other, by)
            )
        )

    def outer_join(
        self, other: DataFrame, by: Sequence[str | tuple[str, str]] | None = None
    ) -> DataFrame:
        return DataFrame(
            self._py_data_frame.outer_join(
                other._py_data_frame, standardize_join_by(self, other, by)
            )
        )

    def left_join(
        self, other: DataFrame, by: Sequence[str | tuple[str, str]] | None = None
    ) -> DataFrame:
        return DataFrame(
            self._py_data_frame.left_join(
                other._py_data_frame, standardize_join_by(self, other, by)
            )
        )

    @overload
    def __getitem__(self, key: tuple[int, str]) -> bool | int | float | str | None:
        pass

    @overload
    def __getitem__(self, key: tuple[int, slice[None] | Sequence[str]]) -> Record:
        pass

    @overload
    def __getitem__(self, key: tuple[slice[int] | Sequence[int], str]) -> Array:
        pass

    @overload
    def __getitem__(
        self, key: tuple[slice[int] | Sequence[int], slice[None] | Sequence[str]]
    ) -> DataFrame:
        pass

    def __getitem__(
        self, key: tuple[int | slice[int] | Sequence[int], str | Sequence[str]]
    ) -> DataFrame | Array | Record | bool | int | float | str:
        row_index, column_index = key

        # Indexing ignores and destroys all group levels
        py_data_frame = self._py_data_frame.ungroup_all()

        match column_index:
            case str():
                return Array(py_data_frame.column(column_index))[row_index]
            case _:  # Sequence[str]
                if column_index == slice(None):
                    selected_data_frame = py_data_frame
                else:
                    selected_data_frame = py_data_frame.select(column_index)

                match row_index:
                    case int():
                        return Record(selected_data_frame.row(row_index))
                    case slice(start=start, stop=stop, step=step):
                        start = start if start is not None else 0
                        stop = stop if stop is not None else self.height
                        step = step if step is not None else 1
                        return DataFrame(selected_data_frame.slice_range0(start, stop, step))
                    case _:  # Sequence[int]
                        return DataFrame(selected_data_frame.slice0(row_index))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataFrame):
            return False
        return self._py_data_frame == other._py_data_frame

    def __repr__(self):
        if self.width == 0:
            return f"DataFrame.columnless({self.height})"
        else:
            column_strs = [f"{name} = {values!r}" for name, values in self.to_dict().items()]
            group_strs = [
                f".group_by({', '.join(map(repr, level))})" for level in self.group_levels
            ]
            return f"DataFrame({', '.join(column_strs)}){''.join(group_strs)}"

    def __str__(self):
        return str(self._py_data_frame)

    @staticmethod
    def read_csv(path: Path, /) -> DataFrame:
        return DataFrame(PyDataFrame.read_csv(str(path)))

    def write_csv(self, path: Path, /) -> None:
        self._py_data_frame.write_csv(str(path))

    @staticmethod
    def from_polars(polars_data_frame: pl.DataFrame) -> DataFrame:
        import pyarrow

        arrow_struct_array = polars_data_frame.to_struct().to_arrow()

        arrow_record_batch = pyarrow.RecordBatch.from_struct_array(arrow_struct_array)

        return DataFrame(PyDataFrame.from_pyarrow_record_batch(arrow_record_batch))

    def to_polars(self) -> pl.DataFrame:
        import polars

        arrow_record_batches = self._py_data_frame.to_pyarrow_record_batches()
        return polars.from_arrow(arrow_record_batches).drop("_dummy")

    @staticmethod
    def from_pandas(pandas_data_frame: pd.DataFrame) -> DataFrame:
        import pyarrow

        arrow_record_batch = pyarrow.RecordBatch.from_pandas(pandas_data_frame)

        return DataFrame(PyDataFrame.from_pyarrow_record_batch(arrow_record_batch))

    def to_pandas(self) -> pd.DataFrame:
        import pyarrow

        record_batches = self._py_data_frame.to_pyarrow_record_batches()
        table = pyarrow.Table.from_batches(record_batches)
        return table.to_pandas().drop("_dummy", axis=1)
