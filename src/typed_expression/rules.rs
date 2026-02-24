use crate::data_type::DataType;
use crate::typed_expression::{ExpressionType, ValidationError};

pub fn promote_expression_types(
    left: ExpressionType,
    right: ExpressionType,
    operation: &str,
) -> Result<ExpressionType, ValidationError> {
    // Check that shapes match
    match (left, right) {
        (ExpressionType::Scalar(left_dt), ExpressionType::Scalar(right_dt)) => {
            let result_dt = promote_numeric_types(left_dt, right_dt, operation)?;
            Ok(ExpressionType::Scalar(result_dt))
        }
        (ExpressionType::Array(left_dt), ExpressionType::Array(right_dt)) => {
            let result_dt = promote_numeric_types(left_dt, right_dt, operation)?;
            Ok(ExpressionType::Array(result_dt))
        }
        // Scalar-Array operations promote to Array
        (ExpressionType::Scalar(left_dt), ExpressionType::Array(right_dt)) => {
            let result_dt = promote_numeric_types(left_dt, right_dt, operation)?;
            Ok(ExpressionType::Array(result_dt))
        }
        (ExpressionType::Array(left_dt), ExpressionType::Scalar(right_dt)) => {
            let result_dt = promote_numeric_types(left_dt, right_dt, operation)?;
            Ok(ExpressionType::Array(result_dt))
        }
    }
}

pub fn promote_numeric_types(
    left: DataType,
    right: DataType,
    operation: &str,
) -> Result<DataType, ValidationError> {
    use DataType::*;

    // Nothing propagates
    if left == Nothing || right == Nothing {
        return Ok(Nothing);
    }

    // If types are the same, no promotion needed
    if left == right {
        return Ok(left);
    }

    match (left, right) {
        // Float64 dominates everything
        (Float64, Integer8 | Integer16 | Integer32 | Integer64)
        | (Integer8 | Integer16 | Integer32 | Integer64, Float64) => Ok(Float64),
        (Float64, Whole8 | Whole16 | Whole32 | Whole64)
        | (Whole8 | Whole16 | Whole32 | Whole64, Float64) => Ok(Float64),
        (Float64, Float32) | (Float32, Float64) => Ok(Float64),

        // Float32 dominates integer types
        (Float32, Integer8 | Integer16 | Integer32 | Integer64)
        | (Integer8 | Integer16 | Integer32 | Integer64, Float32) => Ok(Float32),
        (Float32, Whole8 | Whole16 | Whole32 | Whole64)
        | (Whole8 | Whole16 | Whole32 | Whole64, Float32) => Ok(Float32),

        // Integer promotion hierarchy (signed)
        (Integer64, Integer8 | Integer16 | Integer32)
        | (Integer8 | Integer16 | Integer32, Integer64) => Ok(Integer64),
        (Integer32, Integer8 | Integer16) | (Integer8 | Integer16, Integer32) => Ok(Integer32),
        (Integer16, Integer8) | (Integer8, Integer16) => Ok(Integer16),

        // Whole number promotion hierarchy (unsigned)
        (Whole64, Whole8 | Whole16 | Whole32) | (Whole8 | Whole16 | Whole32, Whole64) => {
            Ok(Whole64)
        }
        (Whole32, Whole8 | Whole16) | (Whole8 | Whole16, Whole32) => Ok(Whole32),
        (Whole16, Whole8) | (Whole8, Whole16) => Ok(Whole16),

        // Mixed signed/unsigned - promote to signed with enough bits
        (Integer64, Whole8 | Whole16 | Whole32 | Whole64)
        | (Whole8 | Whole16 | Whole32 | Whole64, Integer64) => Ok(Integer64),
        (Integer32, Whole8 | Whole16 | Whole32) | (Whole8 | Whole16 | Whole32, Integer32) => {
            Ok(Integer32)
        }
        (Integer16, Whole8 | Whole16) | (Whole8 | Whole16, Integer16) => Ok(Integer16),
        (Integer8, Whole8) | (Whole8, Integer8) => Ok(Integer16), // Need 16 bits for safety
        // Smaller signed with larger unsigned - promote to largest signed
        (Integer8 | Integer16 | Integer32, Whole16 | Whole32 | Whole64)
        | (Whole16 | Whole32 | Whole64, Integer8 | Integer16 | Integer32) => Ok(Integer64),

        // Incompatible types
        _ => Err(ValidationError::IncompatibleTypes {
            operation: operation.to_string(),
            left_type: left,
            right_type: right,
        }),
    }
}

pub fn types_are_comparable(left: DataType, right: DataType) -> bool {
    use DataType::*;

    // Nothing can be compared with anything
    if left == Nothing || right == Nothing {
        return true;
    }

    match (left, right) {
        // Same types are always comparable
        (l, r) if l == r => true,

        // All numeric types are comparable with each other
        (
            Integer8 | Integer16 | Integer32 | Integer64 | Whole8 | Whole16 | Whole32 | Whole64
            | Float32 | Float64,
            Integer8 | Integer16 | Integer32 | Integer64 | Whole8 | Whole16 | Whole32 | Whole64
            | Float32 | Float64,
        ) => true,

        // Booleans can be compared with numeric types (Polars allows this)
        (
            Boolean,
            Integer8 | Integer16 | Integer32 | Integer64 | Whole8 | Whole16 | Whole32 | Whole64
            | Float32 | Float64,
        )
        | (
            Integer8 | Integer16 | Integer32 | Integer64 | Whole8 | Whole16 | Whole32 | Whole64
            | Float32 | Float64,
            Boolean,
        ) => true,

        // Everything else is not comparable
        _ => false,
    }
}
