__all__ = [
    "ArraysNotEqualError",
    "ColumnAlreadyExistsError",
    "DataFramesNotEqualError",
    "DuplicateColumnError",
    "FilterTypeError",
    "FunctionArgumentCountError",
    "FunctionArgumentTypeError",
    "GroupColumnError",
    "GroupIndexOutOfBoundsError",
    "HasGroupsError",
    "IncomparableTypesError",
    "IncompatibleElementTypeError",
    "IncompatibleLengthError",
    "IncompatibleTypeError",
    "IncompatibleTypesError",
    "IndexOutOfBoundsError",
    "NoGroupsError",
    "NonexistentColumnError",
    "NumericTypeNotSatisfiedError",
    "RenameExistingError",
    "TypeMismatchError",
    "UnknownFunctionError",
    "UnknownVariableError",
    "UnmatchedColumnsError",
    "UnmatchedGroupLevelsError",
    "UnmatchedHeightError",
]

from dataclasses import dataclass

from ._tabeline import (
    ArraysNotEqualError,
    ColumnAlreadyExistsError,
    DataFramesNotEqualError,
    DuplicateColumnError,
    FilterTypeError,
    FunctionArgumentCountError,
    FunctionArgumentTypeError,
    GroupColumnError,
    GroupIndexOutOfBoundsError,
    HasGroupsError,
    IncomparableTypesError,
    IncompatibleTypeError,
    IncompatibleTypesError,
    IndexOutOfBoundsError,
    NoGroupsError,
    NonexistentColumnError,
    NumericTypeNotSatisfiedError,
    RenameExistingError,
    TypeMismatchError,
    UnknownFunctionError,
    UnknownVariableError,
    UnmatchedColumnsError,
    UnmatchedGroupLevelsError,
    UnmatchedHeightError,
)


@dataclass(frozen=True, slots=True)
class IncompatibleElementTypeError(TypeError):
    expected_types: list[type]
    item: object
    location_index: int

    def __str__(self) -> str:
        type_names = [t.__name__ for t in self.expected_types]
        return (
            f"Expected all elements to have type {' or '.join(type_names)}, "
            f"but got {self.item} of type {type(self.item)} at index {self.location_index}"
        )


@dataclass(frozen=True, slots=True)
class IncompatibleLengthError(ValueError):
    expected_length: int
    actual_length: int
    column_name: str

    def __str__(self):
        return (
            f"Expected all columns to have length {self.expected_length}, "
            f"but got length {self.actual_length} in column {self.column_name}"
        )
