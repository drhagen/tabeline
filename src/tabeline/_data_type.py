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
        match data_type:
            case pl.Boolean:
                return DataType.Boolean
            case pl.Int8:
                return DataType.Integer8
            case pl.Int16:
                return DataType.Integer16
            case pl.Int32:
                return DataType.Integer32
            case pl.Int64:
                return DataType.Integer64
            case pl.UInt8:
                return DataType.Whole8
            case pl.UInt16:
                return DataType.Whole16
            case pl.UInt32:
                return DataType.Whole32
            case pl.UInt64:
                return DataType.Whole64
            case pl.Float32:
                return DataType.Float32
            case pl.Float64:
                return DataType.Float64
            case pl.Utf8:
                return DataType.String
            case pl.Null:
                return DataType.Nothing
            case _:
                raise TypeError(f"Unsupported Polars data type: {data_type}")

    def to_polars(self) -> pl.DataType:
        match self:
            case DataType.Boolean:
                return pl.Boolean()
            case DataType.Integer8:
                return pl.Int8()
            case DataType.Integer16:
                return pl.Int16()
            case DataType.Integer32:
                return pl.Int32()
            case DataType.Integer64:
                return pl.Int64()
            case DataType.Whole8:
                return pl.UInt8()
            case DataType.Whole16:
                return pl.UInt16()
            case DataType.Whole32:
                return pl.UInt32()
            case DataType.Whole64:
                return pl.UInt64()
            case DataType.Float32:
                return pl.Float32()
            case DataType.Float64:
                return pl.Float64()
            case DataType.String:
                return pl.Utf8()
            case DataType.Nothing:
                return pl.Null()
