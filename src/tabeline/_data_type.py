from __future__ import annotations

__all__ = ["DataType"]

from enum import Enum, auto

import polars as pl


class DataType(Enum):
    Boolean = auto()
    Integer8 = auto()
    Integer16 = auto()
    Integer32 = auto()
    Integer64 = auto()
    Whole8 = auto()
    Whole16 = auto()
    Whole32 = auto()
    Whole64 = auto()
    Float32 = auto()
    Float64 = auto()
    String = auto()
    Nothing = auto()

    @staticmethod
    def from_polars(data_type: pl.DataType, /) -> DataType:
        if data_type == pl.Boolean:
            return DataType.Boolean
        elif data_type == pl.Int8:
            return DataType.Integer8
        elif data_type == pl.Int16:
            return DataType.Integer16
        elif data_type == pl.Int32:
            return DataType.Integer32
        elif data_type == pl.Int64:
            return DataType.Integer64
        elif data_type == pl.UInt8:
            return DataType.Whole8
        elif data_type == pl.UInt16:
            return DataType.Whole16
        elif data_type == pl.UInt32:
            return DataType.Whole32
        elif data_type == pl.UInt64:
            return DataType.Whole64
        elif data_type == pl.Float32:
            return DataType.Float32
        elif data_type == pl.Float64:
            return DataType.Float64
        elif data_type == pl.Utf8:
            return DataType.String
        elif data_type == pl.Null:
            return DataType.Nothing
        else:
            raise TypeError(f"Unsupported Polars data type: {data_type}")

    def to_polars(self) -> pl.DataType:
        if self == DataType.Boolean:
            return pl.Boolean()
        elif self == DataType.Integer8:
            return pl.Int8()
        elif self == DataType.Integer16:
            return pl.Int16()
        elif self == DataType.Integer32:
            return pl.Int32()
        elif self == DataType.Integer64:
            return pl.Int64()
        elif self == DataType.Whole8:
            return pl.UInt8()
        elif self == DataType.Whole16:
            return pl.UInt16()
        elif self == DataType.Whole32:
            return pl.UInt32()
        elif self == DataType.Whole64:
            return pl.UInt64()
        elif self == DataType.Float32:
            return pl.Float32()
        elif self == DataType.Float64:
            return pl.Float64()
        elif self == DataType.String:
            return pl.Utf8()
        elif self == DataType.Nothing:
            return pl.Null()
