use crate::data_type::DataType;
use crate::typed_expression::{ExpressionType, LiteralType, ValidationError};

fn promote_literal_types(left: LiteralType, right: LiteralType) -> LiteralType {
    use LiteralType::*;
    match (left, right) {
        (Whole(_), Whole(v)) => Whole(v),
        (Integer(_), Integer(v)) | (Whole(_), Integer(v)) | (Integer(v), Whole(_)) => Integer(v),
        (Float(v), _) | (_, Float(v)) => Float(v),
    }
}

pub fn promote_expression_types(
    left: ExpressionType,
    right: ExpressionType,
    operation: &str,
) -> Result<ExpressionType, ValidationError> {
    use ExpressionType::*;

    match (left, right) {
        // Literal meets literal
        (Literal(l), Literal(r)) => Ok(Literal(promote_literal_types(l, r))),

        // Whole literal adapts to any concrete numeric type
        (Literal(LiteralType::Whole(_)), Scalar(dt))
        | (Scalar(dt), Literal(LiteralType::Whole(_)))
            if dt.is_numeric() =>
        {
            Ok(Scalar(dt))
        }
        (Literal(LiteralType::Whole(_)), Array(dt))
        | (Array(dt), Literal(LiteralType::Whole(_)))
            if dt.is_numeric() =>
        {
            Ok(Array(dt))
        }

        // Integer literal adapts to signed integer and float types,
        // but promotes whole types to their signed counterpart
        (Literal(LiteralType::Integer(_)), Scalar(dt))
        | (Scalar(dt), Literal(LiteralType::Integer(_)))
            if dt.is_numeric() =>
        {
            Ok(Scalar(dt.to_signed()))
        }
        (Literal(LiteralType::Integer(_)), Array(dt))
        | (Array(dt), Literal(LiteralType::Integer(_)))
            if dt.is_numeric() =>
        {
            Ok(Array(dt.to_signed()))
        }

        // Float literal adapts to float concrete
        (Literal(LiteralType::Float(_)), Scalar(dt))
        | (Scalar(dt), Literal(LiteralType::Float(_)))
            if dt.is_float() =>
        {
            Ok(Scalar(dt))
        }
        (Literal(LiteralType::Float(_)), Array(dt))
        | (Array(dt), Literal(LiteralType::Float(_)))
            if dt.is_float() =>
        {
            Ok(Array(dt))
        }

        // Float literal promotes int/whole to Float64
        (Literal(LiteralType::Float(_)), Scalar(dt))
        | (Scalar(dt), Literal(LiteralType::Float(_)))
            if dt.is_numeric() =>
        {
            Ok(Scalar(DataType::Float64))
        }
        (Literal(LiteralType::Float(_)), Array(dt))
        | (Array(dt), Literal(LiteralType::Float(_)))
            if dt.is_numeric() =>
        {
            Ok(Array(DataType::Float64))
        }

        // Concrete types: delegate to promote_numeric_types
        (Scalar(left_dt), Scalar(right_dt)) => {
            let result_dt = promote_numeric_types(left_dt, right_dt, operation)?;
            Ok(Scalar(result_dt))
        }
        (Array(left_dt), Array(right_dt)) => {
            let result_dt = promote_numeric_types(left_dt, right_dt, operation)?;
            Ok(Array(result_dt))
        }
        // Scalar-Array operations promote to Array
        (Scalar(left_dt), Array(right_dt)) => {
            let result_dt = promote_numeric_types(left_dt, right_dt, operation)?;
            Ok(Array(result_dt))
        }
        (Array(left_dt), Scalar(right_dt)) => {
            let result_dt = promote_numeric_types(left_dt, right_dt, operation)?;
            Ok(Array(result_dt))
        }

        // Incompatible types (e.g. literal with non-numeric)
        _ => Err(ValidationError::IncompatibleTypes {
            operation: operation.to_string(),
            left_type: left.data_type(),
            right_type: right.data_type(),
        }),
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

        // Mixed signed/unsigned - promote to signed at the larger byte size
        (Integer64, Whole8 | Whole16 | Whole32 | Whole64)
        | (Whole8 | Whole16 | Whole32 | Whole64, Integer64) => Ok(Integer64),
        (Integer32, Whole8 | Whole16 | Whole32) | (Whole8 | Whole16 | Whole32, Integer32) => {
            Ok(Integer32)
        }
        (Integer32, Whole64) | (Whole64, Integer32) => Ok(Integer64),
        (Integer16, Whole8 | Whole16) | (Whole8 | Whole16, Integer16) => Ok(Integer16),
        (Integer16, Whole32) | (Whole32, Integer16) => Ok(Integer32),
        (Integer16, Whole64) | (Whole64, Integer16) => Ok(Integer64),
        (Integer8, Whole8) | (Whole8, Integer8) => Ok(Integer8),
        (Integer8, Whole16) | (Whole16, Integer8) => Ok(Integer16),
        (Integer8, Whole32) | (Whole32, Integer8) => Ok(Integer32),
        (Integer8, Whole64) | (Whole64, Integer8) => Ok(Integer64),

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

        // Everything else is not comparable
        _ => false,
    }
}
