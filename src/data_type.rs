use std::fmt;

pub use polars::datatypes::DataType as PolarsDataType;

use pyo3::pyclass;

#[pyclass(frozen, eq, hash)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum DataType {
    Boolean,
    Integer8,
    Integer16,
    Integer32,
    Integer64,
    Whole8,
    Whole16,
    Whole32,
    Whole64,
    Float32,
    Float64,
    String,
    Nothing,
}

impl fmt::Display for DataType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s = match self {
            DataType::Boolean => "Boolean",
            DataType::Integer8 => "Integer8",
            DataType::Integer16 => "Integer16",
            DataType::Integer32 => "Integer32",
            DataType::Integer64 => "Integer64",
            DataType::Whole8 => "Whole8",
            DataType::Whole16 => "Whole16",
            DataType::Whole32 => "Whole32",
            DataType::Whole64 => "Whole64",
            DataType::Float32 => "Float32",
            DataType::Float64 => "Float64",
            DataType::String => "String",
            DataType::Nothing => "Nothing",
        };
        write!(f, "{}", s)
    }
}

impl From<&PolarsDataType> for DataType {
    fn from(polars_data_type: &PolarsDataType) -> Self {
        match polars_data_type {
            PolarsDataType::Boolean => DataType::Boolean,
            PolarsDataType::Int8 => DataType::Integer8,
            PolarsDataType::Int16 => DataType::Integer16,
            PolarsDataType::Int32 => DataType::Integer32,
            PolarsDataType::Int64 => DataType::Integer64,
            PolarsDataType::UInt8 => DataType::Whole8,
            PolarsDataType::UInt16 => DataType::Whole16,
            PolarsDataType::UInt32 => DataType::Whole32,
            PolarsDataType::UInt64 => DataType::Whole64,
            PolarsDataType::Float32 => DataType::Float32,
            PolarsDataType::Float64 => DataType::Float64,
            PolarsDataType::String => DataType::String,
            PolarsDataType::Null => DataType::Nothing,
            _ => {
                panic!(
                    "Error: Unsupported Polars data type: {:?}",
                    polars_data_type
                );
            }
        }
    }
}

impl From<DataType> for PolarsDataType {
    fn from(data_type: DataType) -> Self {
        match data_type {
            DataType::Boolean => PolarsDataType::Boolean,
            DataType::Integer8 => PolarsDataType::Int8,
            DataType::Integer16 => PolarsDataType::Int16,
            DataType::Integer32 => PolarsDataType::Int32,
            DataType::Integer64 => PolarsDataType::Int64,
            DataType::Whole8 => PolarsDataType::UInt8,
            DataType::Whole16 => PolarsDataType::UInt16,
            DataType::Whole32 => PolarsDataType::UInt32,
            DataType::Whole64 => PolarsDataType::UInt64,
            DataType::Float32 => PolarsDataType::Float32,
            DataType::Float64 => PolarsDataType::Float64,
            DataType::String => PolarsDataType::String,
            DataType::Nothing => PolarsDataType::Null,
        }
    }
}
