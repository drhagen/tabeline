from tabeline import DataType

# ruff: noqa: ERA001

# Comment out some types to keep the number of tests reasonable
whole_data_types = [
    DataType.Whole8,
    # DataType.Whole16,
    # DataType.Whole32,
    DataType.Whole64,
]

integer_data_types = [
    DataType.Integer8,
    # DataType.Integer16,
    # DataType.Integer32,
    DataType.Integer64,
]

float_data_types = [
    DataType.Float32,
    DataType.Float64,
]

numeric_types = whole_data_types + integer_data_types + float_data_types

whole_to_whole = [
    (DataType.Whole8, DataType.Whole8),
    # (DataType.Whole16, DataType.Whole16),
    # (DataType.Whole32, DataType.Whole32),
    (DataType.Whole64, DataType.Whole64),
]

integer_to_integer = [
    (DataType.Integer8, DataType.Integer8),
    # (DataType.Integer16, DataType.Integer16),
    # (DataType.Integer32, DataType.Integer32),
    (DataType.Integer64, DataType.Integer64),
]

float_to_float = [
    (DataType.Float32, DataType.Float32),
    (DataType.Float64, DataType.Float64),
]

whole_to_integer = [
    (DataType.Whole8, DataType.Integer8),
    # (DataType.Whole16, DataType.Integer16),
    # (DataType.Whole32, DataType.Integer32),
    (DataType.Whole64, DataType.Integer64),
]

whole_to_float = [
    (DataType.Whole8, DataType.Float64),
    # (DataType.Whole16, DataType.Float64),
    # (DataType.Whole32, DataType.Float64),
    (DataType.Whole64, DataType.Float64),
]

integer_to_float = [
    (DataType.Integer8, DataType.Float64),
    # (DataType.Integer16, DataType.Float64),
    # (DataType.Integer32, DataType.Float64),
    (DataType.Integer64, DataType.Float64),
]

numeric_to_integer = whole_to_integer + integer_to_integer + float_to_float

numeric_to_float = whole_to_float + integer_to_float + float_to_float
