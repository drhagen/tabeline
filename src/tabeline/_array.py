from __future__ import annotations

__all__ = ["Array"]

from collections.abc import Sequence
from typing import TYPE_CHECKING, Iterator, overload

import polars as pl

if TYPE_CHECKING:
    import numpy as np


class Array(Sequence):
    @overload
    def __init__(self, *elements: bool):
        pass

    @overload
    def __init__(self, *elements: int):
        pass

    @overload
    def __init__(self, *elements: float):
        pass

    @overload
    def __init__(self, *elements: str):
        pass

    @overload
    def __init__(self, elements: pl.Array, /):
        pass

    def __init__(self, *elements):
        if len(elements) == 1 and isinstance(elements[0], pl.Series):
            self._array = elements[0]
        else:
            self._array = pl.Series(values=elements)

    @staticmethod
    def from_polars(array: pl.Array, /) -> Array:
        return Array(array)

    def to_polars(self) -> pl.Array:
        return self._array

    @staticmethod
    def from_numpy(array: np.ndarray, /) -> Array:
        return Array(pl.Series(values=array))

    def to_numpy(self) -> np.ndarray:
        return self._array.to_numpy()

    def __len__(self) -> int:
        return len(self._array)

    def __getitem__(self, index: int) -> bool | int | float | str:
        return self._array[index]

    def __iter__(self) -> Iterator[bool | int | float | str]:
        return iter(self._array)

    def __eq__(self, other: object) -> bool:
        # Series equality considers the name of the series, convert to NumPy
        # array compare just values and also consider NaNs equal.
        if isinstance(other, (Array, pl.Series)):
            # Exit early on empty arrays to avoid NumPy/ctypes warning in Python 3.9
            if len(self) == 0 or len(other) == 0:
                return len(self) == len(other)

            return array_equal(self.to_numpy(), other.to_numpy())
        elif isinstance(other, np.ndarray):
            # Exit early on empty arrays to avoid NumPy/ctypes warning in Python 3.9
            if len(self) == 0 or len(other) == 0:
                return len(self) == len(other)

            return array_equal(self.to_numpy(), other)
        return NotImplemented

    def __str__(self) -> str:
        return "[\n" + "".join(f"    {x}" for x in self._array) + "\n]"

    def __repr__(self) -> str:
        return f"Array({', '.join(repr(x) for x in self._array)})"

    def __array__(self) -> np.ndarray:
        return self.to_numpy()


def array_equal(left: np.ndarray, right: np.ndarray) -> bool:
    import numpy as np

    # equal_nan crashes on non-numeric arrays, catch that error and try again
    try:
        return np.array_equal(left, right, equal_nan=True)
    except TypeError:
        return np.array_equal(left, right)
