from __future__ import annotations

__all__ = ["Array"]

from typing import Iterator, overload

import numpy as np
import polars as pl


class Array:
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
        if isinstance(other, (Array, pl.Series)):
            return np.array_equal(self.to_numpy(), other.to_numpy())
        elif isinstance(other, np.ndarray):
            return np.array_equal(self.to_numpy(), other)
        return NotImplemented

    def __str__(self) -> str:
        return "[\n" + "".join(f"    {x}" for x in self._array) + "\n]"

    def __repr__(self) -> str:
        return f"Array({', '.join(repr(x) for x in self._array)})"

    def __array__(self) -> np.ndarray:
        return self.to_numpy()
