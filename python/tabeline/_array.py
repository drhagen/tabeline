from __future__ import annotations

__all__ = ["Array", "Element"]

from collections.abc import Sequence
from typing import TYPE_CHECKING, Generic, TypeVar, overload

from ._tabeline import DataType, PyArray
from .exceptions import IncompatibleElementTypeError

Element = TypeVar("Element", bound=DataType)

if TYPE_CHECKING:
    import numpy as np
    import polars as pl


def py_array_from_sequence(elements: Sequence[Element], data_type: DataType) -> PyArray:
    # This is split out so that __init__ and from_sequence can share the logic,
    # when they can't call each other
    match data_type:
        case None:
            inferred_data_type = DataType.Nothing
            parsed_elements = list(elements)
            for i, item in enumerate(parsed_elements):
                match inferred_data_type:
                    case DataType.Nothing:
                        match item:
                            case None:
                                pass
                            case bool():
                                inferred_data_type = DataType.Boolean
                            case int():
                                inferred_data_type = DataType.Integer64
                            case float():
                                inferred_data_type = DataType.Float64
                            case str():
                                inferred_data_type = DataType.String
                            case _:
                                raise IncompatibleElementTypeError(
                                    [bool, int, float, str, type(None)], item, i
                                )
                    case DataType.Boolean:
                        match item:
                            case None:
                                pass
                            case bool():
                                pass
                            case _:
                                raise IncompatibleElementTypeError([bool, type(None)], item, i)
                    case DataType.Integer64:
                        match item:
                            case None:
                                pass
                            case int():
                                pass
                            case float():
                                for j in range(i + 1):
                                    element_j = parsed_elements[j]
                                    parsed_elements[j] = (
                                        float(parsed_elements[j])
                                        if element_j is not None
                                        else None
                                    )
                                inferred_data_type = DataType.Float64
                            case _:
                                raise IncompatibleElementTypeError(
                                    [int, float, type(None)], item, i
                                )
                    case DataType.Float64:
                        match item:
                            case None:
                                pass
                            case int():
                                parsed_elements[i] = float(item)
                            case float():
                                pass
                            case _:
                                raise IncompatibleElementTypeError(
                                    [int, float, type(None)], item, i
                                )
                    case DataType.String:
                        match item:
                            case None:
                                pass
                            case str():
                                pass
                            case _:
                                raise IncompatibleElementTypeError([str, type(None)], item, i)
                    case _:
                        raise NotImplementedError()
        case _:
            inferred_data_type = data_type
            parsed_elements = list(elements)
            match data_type:
                case DataType.Nothing:
                    for i, item in enumerate(parsed_elements):
                        match item:
                            case None:
                                pass
                            case _:
                                raise IncompatibleElementTypeError([type(None)], item, i)
                case DataType.Boolean:
                    for i, item in enumerate(parsed_elements):
                        match item:
                            case None:
                                pass
                            case bool():
                                pass
                            case _:
                                raise IncompatibleElementTypeError([bool, type(None)], item, i)
                case (
                    DataType.Integer8
                    | DataType.Integer16
                    | DataType.Integer32
                    | DataType.Integer64
                    | DataType.Whole8
                    | DataType.Whole16
                    | DataType.Whole32
                    | DataType.Whole64
                ):
                    for i, item in enumerate(parsed_elements):
                        match item:
                            case None:
                                pass
                            case int():
                                pass
                            case _:
                                raise IncompatibleElementTypeError(
                                    [int, float, type(None)], item, i
                                )
                case DataType.Float32 | DataType.Float64:
                    for i, item in enumerate(parsed_elements):
                        match item:
                            case None:
                                pass
                            case int():
                                parsed_elements[i] = float(item)
                            case float():
                                pass
                            case _:
                                raise IncompatibleElementTypeError(
                                    [int, float, type(None)], item, i
                                )
                case DataType.String:
                    for i, item in enumerate(parsed_elements):
                        match item:
                            case None:
                                pass
                            case str():
                                pass
                            case _:
                                raise IncompatibleElementTypeError([str, type(None)], item, i)
                case _:
                    raise TypeError(
                        f"Array.from_sequence not implemented for data type {data_type}"
                    )

    return PyArray.from_list(parsed_elements, data_type=inferred_data_type)


class Array(Generic[Element]):
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
    def __init__(self, elements: PyArray) -> None:
        pass

    def __init__(self, *elements, data_type: DataType | None = None) -> None:
        if len(elements) > 0 and isinstance(elements[0], PyArray):
            if len(elements) != 1:
                raise TypeError(
                    "Passing a PyArray is the private constructor, "
                    "which requires exactly one argument"
                )
            if data_type is not None:
                raise TypeError(
                    "Passing a PyArray is the private constructor, "
                    "which does not allow setting the data type"
                )

            rust_array = elements[0]
        else:
            rust_array = py_array_from_sequence(elements, data_type=data_type)

        self._py_array = rust_array

    @property
    def data_type(self) -> DataType:
        return self._py_array.data_type

    def __eq__(self, value):
        if not isinstance(value, Array):
            return False
        else:
            return self._py_array == value._py_array

    def __len__(self) -> int:
        return len(self._py_array)

    @overload
    def __getitem__(self, key: int) -> bool | int | float | str | None:
        pass

    @overload
    def __getitem__(self, key: slice[int] | Sequence[int]) -> Array:
        pass

    def __getitem__(self, index: int | slice) -> Element:
        match index:
            case int():
                return self._py_array.item(index)
            case slice(start=start, stop=stop, step=step):
                start = start if start is not None else 0
                stop = stop if stop is not None else len(self)
                step = step if step is not None else 1
                return Array(self._py_array.slice_range0(start, stop, step))
            case _:  # Sequence[int]
                return Array(self._py_array.slice0(index))

    def __iter__(self):
        return iter(self._py_array)

    def __str__(self) -> str:
        return "[\n" + "".join(f"    {x}" for x in self._py_array) + "\n]"

    def __repr__(self) -> str:
        return f"Array[{self.data_type}]({', '.join(repr(x) for x in self._py_array)})"

    @staticmethod
    def from_sequence(
        elements: Sequence[Element], /, *, data_type: DataType | None = None
    ) -> Array[Element]:
        """Construct an Array from a sequence of elements.

        The desired data type can be provided explicitly. If it is, the elements will be checked
        that they are of a compatible Python type. Elements of type `int` will be implicitly
        converted to `float`s if a float type is requested. No others conversions will occur.

        If no data type is provided, the data type will be inferred from the elements. A mixture of
        ints and floats will be inferred as floats. All other types will be inferred as follows:

        - `bool`: `DataType.Bool`
        - `int`: `DataType.Integer64`
        - `float`: `DataType.Float64`
        - `str`: `DataType.String`

        All types can also have `None` as a value. If all elements are `None`, including an empty
        sequence, the data type will be `DataType.Nothing`.
        """
        return Array(py_array_from_sequence(elements, data_type=data_type))

    @staticmethod
    def from_polars(series: pl.Series) -> Array:
        """Construct an Array from a polars Series."""
        return Array(PyArray.from_pyarrow_array(series.to_arrow()))

    def to_polars(self) -> pl.Series:
        """Convert the Array to a polars Series."""
        import polars

        return polars.from_arrow(self._py_array.to_pyarrow_array())

    @staticmethod
    def from_numpy(array: np.ndarray) -> Array:
        """Construct an Array from a numpy array."""
        import pyarrow

        return Array(PyArray.from_pyarrow_array(pyarrow.array(array)))

    def to_numpy(self) -> np.ndarray:
        """Convert the Array to a numpy array."""
        # PyArrow does not support zero-copy for all data types
        return self._py_array.to_pyarrow_array().to_numpy(zero_copy_only=False)

    def __class_getitem__(cls, data_type: DataType) -> SpecializedArray:
        return SpecializedArray(data_type)


class SpecializedArray:
    def __init__(self, data_type: DataType, /) -> None:
        self.data_type = data_type

    def __call__(self, *elements: object) -> Array:
        return Array.from_sequence(elements, data_type=self.data_type)
