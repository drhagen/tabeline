from tabeline import DataType

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
