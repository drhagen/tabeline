use crate::data_type::DataType;
use crate::expression::Expression;
use crate::typed_expression::{
    promote_expression_types, promote_numeric_types, types_are_comparable, DataFrameType,
    ExpressionType, TypedExpression, ValidationError,
};
use std::sync::Arc;

impl Expression {
    pub fn validate(&self, df_type: &DataFrameType) -> Result<TypedExpression, ValidationError> {
        match self {
            // Literals - always scalar types (type is inferred from the variant)
            Expression::NullLiteral => Ok(TypedExpression::NullLiteral),

            Expression::BooleanLiteral { value } => {
                Ok(TypedExpression::BooleanLiteral { value: *value })
            }

            Expression::IntegerLiteral { value } => {
                Ok(TypedExpression::IntegerLiteral { value: *value })
            }

            Expression::FloatLiteral { value } => {
                Ok(TypedExpression::FloatLiteral { value: *value })
            }

            Expression::StringLiteral { value } => Ok(TypedExpression::StringLiteral {
                value: value.clone(),
            }),

            // Variables - array types resolved from DataFrameType
            Expression::Variable { name } => {
                let expression_type = df_type.column_expression_type(name).ok_or_else(|| {
                    ValidationError::UnknownVariable {
                        name: name.clone(),
                        available: df_type.column_names(),
                    }
                })?;

                Ok(TypedExpression::Variable {
                    name: name.clone(),
                    expression_type,
                })
            }

            // Unary operators - preserve type
            Expression::Positive { content } => {
                let typed_content = content.validate(df_type)?;
                let expression_type = typed_content.expression_type();

                // Positive only works with numeric types
                let data_type = expression_type.data_type();
                if !data_type.is_numeric() {
                    return Err(ValidationError::NumericTypeNotSatisfied {
                        operation: "+_".to_string(),
                        actual: data_type,
                    });
                }

                Ok(TypedExpression::Positive {
                    content: Arc::new(typed_content),
                    expression_type,
                })
            }

            Expression::Negative { content } => {
                let typed_content = content.validate(df_type)?;
                let expression_type = typed_content.expression_type();

                // Negative only works with numeric types
                let data_type = expression_type.data_type();
                if !data_type.is_numeric() {
                    return Err(ValidationError::NumericTypeNotSatisfied {
                        operation: "-_".to_string(),
                        actual: data_type,
                    });
                }

                // Upcast unsigned types to signed (negation of unsigned is invalid)
                let signed_dt = data_type.to_signed();
                let result_type = expression_type.with_data_type(signed_dt);

                Ok(TypedExpression::Negative {
                    content: Arc::new(typed_content.cast_if_needed(signed_dt)),
                    expression_type: result_type,
                })
            }

            Expression::Not { content } => {
                let typed_content = content.validate(df_type)?;
                let expression_type = typed_content.expression_type();

                // Not only works with boolean types (Nothing is allowed and propagates)
                let data_type = expression_type.data_type();
                if data_type != DataType::Boolean && data_type != DataType::Nothing {
                    return Err(ValidationError::TypeMismatch {
                        operation: "~_".to_string(),
                        expected: DataType::Boolean,
                        actual: data_type,
                    });
                }

                Ok(TypedExpression::Not {
                    content: Arc::new(typed_content),
                    expression_type,
                })
            }

            // Arithmetic operators
            Expression::Add { left, right } => {
                validate_binary_arithmetic(left, right, df_type, "addition", |l, r, et| {
                    TypedExpression::Add {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            Expression::Subtract { left, right } => {
                validate_binary_arithmetic(left, right, df_type, "subtraction", |l, r, et| {
                    let signed_dt = et.data_type().to_signed();
                    TypedExpression::Subtract {
                        left: Arc::new(l.cast_if_needed(signed_dt)),
                        right: Arc::new(r.cast_if_needed(signed_dt)),
                        expression_type: et.with_data_type(signed_dt),
                    }
                })
            }

            Expression::Multiply { left, right } => {
                validate_binary_arithmetic(left, right, df_type, "multiplication", |l, r, et| {
                    TypedExpression::Multiply {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            Expression::TrueDivide { left, right } => {
                validate_binary_arithmetic(left, right, df_type, "division", |l, r, et| {
                    let float_dt = l
                        .expression_type()
                        .data_type()
                        .promote_to_float(r.expression_type().data_type());
                    TypedExpression::TrueDivide {
                        left: Arc::new(l.cast_if_needed(float_dt)),
                        right: Arc::new(r.cast_if_needed(float_dt)),
                        expression_type: et.with_data_type(float_dt),
                    }
                })
            }

            Expression::FloorDivide { left, right } => {
                validate_binary_arithmetic(left, right, df_type, "floor division", |l, r, et| {
                    TypedExpression::FloorDivide {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            Expression::Mod { left, right } => {
                validate_binary_arithmetic(left, right, df_type, "modulo", |l, r, et| {
                    TypedExpression::Mod {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            Expression::Power { left, right } => {
                let typed_left = left.validate(df_type)?;
                let typed_right = right.validate(df_type)?;
                let left_type = typed_left.expression_type();
                let right_type = typed_right.expression_type();

                if !left_type.data_type().is_numeric() {
                    return Err(ValidationError::NumericTypeNotSatisfied {
                        operation: "exponentiation".to_string(),
                        actual: left_type.data_type(),
                    });
                }
                if !right_type.data_type().is_numeric() {
                    return Err(ValidationError::NumericTypeNotSatisfied {
                        operation: "exponentiation".to_string(),
                        actual: right_type.data_type(),
                    });
                }

                // Determine result shape from promotion
                let result_type =
                    promote_expression_types(left_type, right_type, "exponentiation")?;

                // Apply literal adaptation and determine exponent wholeness.
                // For literals, the adapted type determines wholeness.
                // For non-literals, the original type determines wholeness.
                let effective_left_dt;
                let effective_right_dt;
                let exponent_is_whole;
                if typed_left.is_literal() && !typed_right.is_literal() {
                    if typed_left.is_float_literal() && !right_type.data_type().is_float() {
                        effective_left_dt = result_type.data_type();
                        effective_right_dt = result_type.data_type();
                    } else {
                        effective_left_dt = right_type.data_type();
                        effective_right_dt = right_type.data_type();
                    }
                    exponent_is_whole = right_type.data_type().is_whole();
                } else if typed_right.is_literal() && !typed_left.is_literal() {
                    if typed_right.is_float_literal() && !left_type.data_type().is_float() {
                        effective_left_dt = result_type.data_type();
                        effective_right_dt = result_type.data_type();
                    } else {
                        effective_left_dt = left_type.data_type();
                        effective_right_dt = left_type.data_type();
                    }
                    // Integer literal exponents are always treated as whole
                    exponent_is_whole = !typed_right.is_float_literal();
                } else {
                    effective_left_dt = left_type.data_type();
                    effective_right_dt = right_type.data_type();
                    exponent_is_whole = right_type.data_type().is_whole();
                }

                if exponent_is_whole {
                    // anything ** whole → preserves base type
                    let base_dt = effective_left_dt;
                    Ok(TypedExpression::Power {
                        left: Arc::new(typed_left.cast_if_needed(base_dt)),
                        right: Arc::new(typed_right.cast_if_needed(base_dt)),
                        expression_type: result_type.with_data_type(base_dt),
                    })
                } else {
                    // anything ** int/float → float operation
                    let promoted_dt = effective_left_dt
                        .promote_to_float(effective_right_dt);
                    Ok(TypedExpression::Power {
                        left: Arc::new(typed_left.cast_if_needed(promoted_dt)),
                        right: Arc::new(typed_right.cast_if_needed(promoted_dt)),
                        expression_type: result_type.with_data_type(promoted_dt),
                    })
                }
            }

            // Comparison operators
            Expression::Equal { left, right } => {
                validate_comparison(left, right, df_type, "equality", |l, r, et| {
                    TypedExpression::Equal {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            Expression::NotEqual { left, right } => {
                validate_comparison(left, right, df_type, "inequality", |l, r, et| {
                    TypedExpression::NotEqual {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            Expression::GreaterThan { left, right } => {
                validate_comparison(left, right, df_type, "greater than", |l, r, et| {
                    TypedExpression::GreaterThan {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            Expression::GreaterThanOrEqual { left, right } => {
                validate_comparison(left, right, df_type, "greater than or equal", |l, r, et| {
                    TypedExpression::GreaterThanOrEqual {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            Expression::LessThan { left, right } => {
                validate_comparison(left, right, df_type, "less than", |l, r, et| {
                    TypedExpression::LessThan {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            Expression::LessThanOrEqual { left, right } => {
                validate_comparison(left, right, df_type, "less than or equal", |l, r, et| {
                    TypedExpression::LessThanOrEqual {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            // Logical operators
            Expression::And { left, right } => {
                validate_logical(left, right, df_type, "and", |l, r, et| {
                    TypedExpression::And {
                        left: Arc::new(l),
                        right: Arc::new(r),
                        expression_type: et,
                    }
                })
            }

            Expression::Or { left, right } => {
                validate_logical(left, right, df_type, "or", |l, r, et| TypedExpression::Or {
                    left: Arc::new(l),
                    right: Arc::new(r),
                    expression_type: et,
                })
            }

            // Call - validate function and return typed version
            Expression::Call { name, arguments } => {
                let typed_call =
                    crate::function::validate_function(name, arguments.clone(), df_type)?;
                Ok(TypedExpression::Call { call: typed_call })
            }
        }
    }
}

fn validate_binary_arithmetic<F>(
    left: &Expression,
    right: &Expression,
    df_type: &DataFrameType,
    operation: &str,
    constructor: F,
) -> Result<TypedExpression, ValidationError>
where
    F: FnOnce(TypedExpression, TypedExpression, ExpressionType) -> TypedExpression,
{
    let typed_left = left.validate(df_type)?;
    let typed_right = right.validate(df_type)?;

    let left_type = typed_left.expression_type();
    let right_type = typed_right.expression_type();

    // Check that both operands are numeric
    if !left_type.data_type().is_numeric() {
        return Err(ValidationError::NumericTypeNotSatisfied {
            operation: operation.to_string(),
            actual: left_type.data_type(),
        });
    }

    if !right_type.data_type().is_numeric() {
        return Err(ValidationError::NumericTypeNotSatisfied {
            operation: operation.to_string(),
            actual: right_type.data_type(),
        });
    }

    // Promote types (handles scalar/array broadcasting)
    let result_type = promote_expression_types(left_type, right_type, operation)?;

    // Scalar literals adapt to the other operand's type rather than widening it.
    // Integer literals adapt to any numeric type; float literals adapt to float types only.
    let result_type = if typed_left.is_literal() && !typed_right.is_literal() {
        if typed_left.is_float_literal()
            && !right_type.data_type().is_float()
        {
            result_type
        } else {
            result_type.with_data_type(right_type.data_type())
        }
    } else if typed_right.is_literal() && !typed_left.is_literal() {
        if typed_right.is_float_literal()
            && !left_type.data_type().is_float()
        {
            result_type
        } else {
            result_type.with_data_type(left_type.data_type())
        }
    } else {
        result_type
    };

    // Cast operands to promoted type
    let result_dt = result_type.data_type();
    let typed_left = typed_left.cast_if_needed(result_dt);
    let typed_right = typed_right.cast_if_needed(result_dt);

    Ok(constructor(typed_left, typed_right, result_type))
}

fn validate_comparison<F>(
    left: &Expression,
    right: &Expression,
    df_type: &DataFrameType,
    operation: &str,
    constructor: F,
) -> Result<TypedExpression, ValidationError>
where
    F: FnOnce(TypedExpression, TypedExpression, ExpressionType) -> TypedExpression,
{
    let typed_left = left.validate(df_type)?;
    let typed_right = right.validate(df_type)?;

    let left_type = typed_left.expression_type();
    let right_type = typed_right.expression_type();

    // Check that types are comparable
    if !types_are_comparable(left_type.data_type(), right_type.data_type()) {
        return Err(ValidationError::IncomparableTypes {
            operation: operation.to_string(),
            left_type: left_type.data_type(),
            right_type: right_type.data_type(),
        });
    }

    // Cast operands to common type for numeric comparisons.
    // Scalar literals adapt to the other operand's type.
    let (typed_left, typed_right) = if left_type.data_type() != right_type.data_type()
        && left_type.data_type().is_numeric()
        && right_type.data_type().is_numeric()
    {
        if typed_left.is_literal() && !typed_right.is_literal() {
            if typed_left.is_float_literal()
                && !right_type.data_type().is_float()
            {
                let promoted = promote_numeric_types(
                    left_type.data_type(),
                    right_type.data_type(),
                    operation,
                )?;
                (
                    typed_left.cast_if_needed(promoted),
                    typed_right.cast_if_needed(promoted),
                )
            } else {
                (
                    typed_left.cast_if_needed(right_type.data_type()),
                    typed_right,
                )
            }
        } else if typed_right.is_literal() && !typed_left.is_literal() {
            if typed_right.is_float_literal()
                && !left_type.data_type().is_float()
            {
                let promoted = promote_numeric_types(
                    left_type.data_type(),
                    right_type.data_type(),
                    operation,
                )?;
                (
                    typed_left.cast_if_needed(promoted),
                    typed_right.cast_if_needed(promoted),
                )
            } else {
                (
                    typed_left,
                    typed_right.cast_if_needed(left_type.data_type()),
                )
            }
        } else {
            let promoted = promote_numeric_types(
                left_type.data_type(),
                right_type.data_type(),
                operation,
            )?;
            (
                typed_left.cast_if_needed(promoted),
                typed_right.cast_if_needed(promoted),
            )
        }
    } else {
        (typed_left, typed_right)
    };

    // Result is Boolean, but preserves scalar/array shape from operands
    let result_type = match (left_type, right_type) {
        (ExpressionType::Scalar(_), ExpressionType::Scalar(_)) => {
            ExpressionType::Scalar(DataType::Boolean)
        }
        _ => ExpressionType::Array(DataType::Boolean), // Any array operand makes result array
    };

    Ok(constructor(typed_left, typed_right, result_type))
}

fn validate_logical<F>(
    left: &Expression,
    right: &Expression,
    df_type: &DataFrameType,
    operation: &str,
    constructor: F,
) -> Result<TypedExpression, ValidationError>
where
    F: FnOnce(TypedExpression, TypedExpression, ExpressionType) -> TypedExpression,
{
    let typed_left = left.validate(df_type)?;
    let typed_right = right.validate(df_type)?;

    let left_type = typed_left.expression_type();
    let right_type = typed_right.expression_type();

    // Both operands must be Boolean (Nothing is allowed and propagates)
    if left_type.data_type() != DataType::Boolean && left_type.data_type() != DataType::Nothing {
        return Err(ValidationError::TypeMismatch {
            operation: operation.to_string(),
            expected: DataType::Boolean,
            actual: left_type.data_type(),
        });
    }

    if right_type.data_type() != DataType::Boolean && right_type.data_type() != DataType::Nothing {
        return Err(ValidationError::TypeMismatch {
            operation: operation.to_string(),
            expected: DataType::Boolean,
            actual: right_type.data_type(),
        });
    }

    // Result is Boolean, preserves scalar/array shape
    let result_type = match (left_type, right_type) {
        (ExpressionType::Scalar(_), ExpressionType::Scalar(_)) => {
            ExpressionType::Scalar(DataType::Boolean)
        }
        _ => ExpressionType::Array(DataType::Boolean), // Any array operand makes result array
    };

    Ok(constructor(typed_left, typed_right, result_type))
}
