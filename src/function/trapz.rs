use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};

fn compute_trapz(args: &mut [Column]) -> PolarsResult<Column> {
    let t = &args[0];
    let t = t.f64()?;

    let y = &args[1];
    let y = y.f64()?;

    // Check t values are not null and monotonically increasing
    let mut t_vec = Vec::new();
    let mut prev = f64::NEG_INFINITY;
    for i in 0..t.len() {
        match t.get(i) {
            Some(value) => {
                if value < prev {
                    return Err(PolarsError::ComputeError(
                        "Expected t of trapz to be weakly monotonically increasing, but it was not"
                            .into(),
                    ));
                }
                prev = value;
                t_vec.push(value);
            }
            None => {
                return Err(PolarsError::ComputeError(
                    "Expected no nulls in t of trapz, but they were found".into(),
                ))
            }
        }
    }

    // Return null on null values in y
    if y.is_null().any() {
        return Ok(Column::new_scalar(
            "".into(),
            Scalar::new(DataType::Float64, AnyValue::Null),
            1,
        ));
    }

    // Compute trapezoid rule
    let mut sum = 0.0;
    for i in 1..t.len() {
        let x0 = t.get(i - 1).unwrap();
        let x1 = t.get(i).unwrap();
        let y0 = y.get(i - 1).unwrap();
        let y1 = y.get(i).unwrap();

        sum += (x1 - x0) * (y0 + y1);
    }

    Ok(Column::new_scalar(
        "".into(),
        Scalar::new(DataType::Float64, AnyValue::Float64(0.5 * sum)),
        1,
    ))
}

#[derive(Debug, Clone, PartialEq)]
pub struct Trapz {
    pub t: Arc<TypedExpression>,
    pub y: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Trapz {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 2 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "trapz".to_string(),
                expected: 2,
                actual: arguments.len(),
            });
        }

        let t = Arc::new(arguments[0].validate(df_type)?);
        let y = Arc::new(arguments[1].validate(df_type)?);

        let t_type = t.expression_type();
        let y_type = y.expression_type();

        // Both arguments must be numeric
        if !t_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "trapz".to_string(),
                parameter: "t".to_string(),
                expected: "numeric type".to_string(),
                actual: t_type.data_type(),
            });
        }
        if !y_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "trapz".to_string(),
                parameter: "y".to_string(),
                expected: "numeric type".to_string(),
                actual: y_type.data_type(),
            });
        }

        // Both arguments must be arrays
        if !t_type.is_array() {
            return Err(ValidationError::FunctionArgumentType {
                function: "trapz".to_string(),
                parameter: "t".to_string(),
                expected: "array type".to_string(),
                actual: t_type.data_type(),
            });
        }
        if !y_type.is_array() {
            return Err(ValidationError::FunctionArgumentType {
                function: "trapz".to_string(),
                parameter: "y".to_string(),
                expected: "array type".to_string(),
                actual: y_type.data_type(),
            });
        }

        // Result type is Float64 scalar (trapz is an aggregation)
        Ok(Arc::new(Trapz {
            t,
            y,
            expression_type: ExpressionType::Scalar(crate::data_type::DataType::Float64),
        }) as Arc<dyn Function>)
    }
}

impl Function for Trapz {
    fn to_polars(&self) -> Expr {
        apply_multiple(
            compute_trapz,
            &[
                self.t.to_polars().cast(DataType::Float64),
                self.y.to_polars().cast(DataType::Float64),
            ],
            |_, fields| Ok(fields[0].clone()),
            true,
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Trapz {
            t: Arc::new(self.t.substitute(substitutions)),
            y: Arc::new(self.y.substitute(substitutions)),
            expression_type: self.expression_type,
        })
    }

    fn expression_type(&self) -> ExpressionType {
        self.expression_type
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Trapz>() {
            self.t == other.t && self.y == other.y && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "trapz"
    }
}
