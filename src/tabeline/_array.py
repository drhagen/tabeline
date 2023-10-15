from __future__ import annotations

__all__ = ["Array"]

from collections.abc import Sequence
from typing import Generic, Iterator, TypeVar, overload

import numpy as np
import polars as pl
from polars.exceptions import InvalidOperationError

from ._data_type import DataType

Element = TypeVar("Element", bound=DataType)


class Array(Sequence, Generic[Element]):
    @overload
    def __init__(self, *elements: bool | None, data_type: DataType | None = None) -> None:
        pass

    @overload
    def __init__(self, *elements: int | None, data_type: DataType | None = None) -> None:
        pass

    @overload
    def __init__(self, *elements: float | int | None, data_type: DataType | None = None) -> None:
        pass

    @overload
    def __init__(self, *elements: str | None, data_type: DataType | None = None) -> None:
        pass

    @overload
    def __init__(self, elements: pl.Array, /, *, data_type: DataType | None = None) -> None:
        pass

    def __init__(self, *elements, data_type: DataType | None = None) -> None:
        if len(elements) > 0 and isinstance(elements[0], pl.Series):
            if len(elements) != 1:
                raise TypeError(
                    "Passing a Series is the private constructor, "
                    "which requires exactly one argument"
                )
            if data_type is not None:
                raise TypeError(
                    "Passing a Series is the private constructor, "
                    "which does not allow setting the data type"
                )

            series = elements[0]

            # Extract data type from Polars dtype
            data_type = DataType.from_polars(series.dtype)
        else:
            data_type = coerce_default_element_type(default_element_type(elements), data_type)
            series = pl.Series(values=elements, dtype=data_type.to_polars())

        self.data_type = data_type
        self._series = series

    @staticmethod
    def from_sequence(
        sequence: Sequence[None | bool | int | float | str],
        /,
        *,
        data_type: DataType | None = None,
    ) -> Array:
        return Array(*sequence, data_type=data_type)

    @staticmethod
    def from_polars(array: pl.Array, /) -> Array:
        return Array(array)

    def to_polars(self) -> pl.Array:
        return self._series

    @staticmethod
    def from_numpy(array: np.ndarray, /) -> Array:
        return Array(pl.Series(values=array))

    def to_numpy(self) -> np.ndarray:
        return self._series.to_numpy(use_pyarrow=False)

    def __len__(self) -> int:
        return len(self._series)

    def __getitem__(self, index: int) -> bool | int | float | str:
        return self._series[index]

    def __iter__(self) -> Iterator[bool | int | float | str]:
        return iter(self._series)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (Array, pl.Series)):
            # Series.series_equal does not consider NaNs equal, so we have to
            # try to find the NaNs and make those elements equal. But not all
            # data types support NaNs, so bail when is_nan fails.

            self_series = self.to_polars()

            if isinstance(other, Array):
                other_series = other.to_polars()
            else:
                other_series = other

            equal_elements = self_series.eq_missing(other_series)

            try:
                self_nan = self_series.is_nan().fill_null(False)
            except InvalidOperationError:
                return equal_elements.all()

            try:
                other_nan = other_series.is_nan().fill_null(False)
            except InvalidOperationError:
                return equal_elements.all()

            return (equal_elements | (self_nan & other_nan)).all()
        elif isinstance(other, np.ndarray):
            # Exit early on empty arrays to avoid NumPy/ctypes warning in Python 3.9
            if len(self) == 0 or len(other) == 0:
                return len(self) == len(other)

            return array_equal(self.to_numpy(), other)
        return NotImplemented

    def __str__(self) -> str:
        return "[\n" + "".join(f"    {x}" for x in self._series) + "\n]"

    def __repr__(self) -> str:
        return f"Array({', '.join(repr(x) for x in self._series)})"

    def __array__(self) -> np.ndarray:
        return self.to_numpy()

    def __class_getitem__(cls, data_type: DataType) -> SpecializedArray:
        return SpecializedArray(data_type)


class SpecializedArray:
    def __init__(self, data_type: DataType, /) -> None:
        self.data_type = data_type

    def __call__(self, *elements: object) -> Array:
        return Array(*elements, data_type=self.data_type)


def array_equal(left: np.ndarray, right: np.ndarray) -> bool:
    import numpy as np

    # equal_nan crashes on non-numeric arrays, catch that error and try again
    try:
        return np.array_equal(left, right, equal_nan=True)
    except TypeError:
        return np.array_equal(left, right)


def default_element_type(
    sequence: Sequence[bool | None]
    | Sequence[int | None]
    | Sequence[float | int | None]
    | Sequence[str | None],
) -> DataType.Boolean | DataType.Integer64 | DataType.Float64 | DataType.String | DataType.Nothing:
    # Only a subset of data types are possible when converting Python types
    best_type: (
        DataType.Boolean
        | DataType.Integer64
        | DataType.Float64
        | DataType.String
        | DataType.Nothing
    ) = DataType.Nothing

    for element in sequence:
        if best_type == DataType.Nothing:
            if element is None:
                pass
            elif isinstance(element, bool):
                best_type = DataType.Boolean
            elif isinstance(element, int):
                best_type = DataType.Integer64
            elif isinstance(element, float):
                best_type = DataType.Float64
            elif isinstance(element, str):
                best_type = DataType.String
            else:
                raise TypeError(
                    f"Expected bool, int, float, str, or None, but got {type(element)}: {element}"
                )
        elif best_type == DataType.Boolean:
            if element is None or isinstance(element, bool):
                pass
            else:
                raise TypeError(f"Expected bool, but got {type(element)}: {element}")
        elif best_type == DataType.Integer64:
            if element is None or isinstance(element, int):
                pass
            elif isinstance(element, float):
                best_type = DataType.Float64
            else:
                raise TypeError(f"Expected int, but got {type(element)}: {element}")
        elif best_type == DataType.Float64:
            if element is None or isinstance(element, int) or isinstance(element, float):
                pass
            else:
                raise TypeError(f"Expected int or float, but got {type(element)}: {element}")
        elif best_type == DataType.String:
            if element is None or isinstance(element, str):
                pass
            else:
                raise TypeError(f"Expected str, but got {type(element)}: {element}")

    return best_type


def coerce_default_element_type(
    default: DataType.Boolean
    | DataType.Integer64
    | DataType.Float64
    | DataType.String
    | DataType.Nothing,
    given: DataType | None,
) -> DataType:
    if given is None:
        return default
    elif default == DataType.Boolean and given == DataType.Boolean:
        return given
    elif default == DataType.Integer64 and given in [
        DataType.Integer8,
        DataType.Integer16,
        DataType.Integer32,
        DataType.Integer64,
        DataType.Whole8,
        DataType.Whole16,
        DataType.Whole32,
        DataType.Whole64,
        DataType.Float32,
        DataType.Float64,
    ]:
        return given
    elif default == DataType.Float64 and given in [DataType.Float32, DataType.Float64]:
        return given
    elif default == DataType.String and given == DataType.String:
        return given
    elif default == DataType.Nothing and given == DataType.Nothing:
        return given
    else:
        raise TypeError(f"Expected data_type to be compatible with {default}, but got {given}")
