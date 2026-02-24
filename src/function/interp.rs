use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};

fn interpolate(args: &mut [Column]) -> PolarsResult<Column> {
    let t = &args[0];
    let t = t.f64()?;

    let ts = &args[1];
    let ts = ts.f64()?;

    let ys = &args[2];
    let ys = ys.f64()?;

    if ts.len() != ys.len() {
        return Err(PolarsError::ComputeError(
            format!("Expected ts and ys of interp to have the same length, but length of ts is {} and length of ys is {}", ts.len(), ys.len()).into(),
        ));
    }

    if ts.is_empty() {
        return Err(PolarsError::ComputeError(
            "Expected ts and ys of interp to be non-empty, but they were empty"
                .to_string()
                .into(),
        ));
    }

    // Check ts are not null and monotonically increasing
    let mut ts_vec = Vec::new();
    let mut prev = f64::NEG_INFINITY;
    for i in 0..ts.len() {
        match ts.get(i) {
            Some(value) => {
                if value < prev {
                    return Err(PolarsError::ComputeError(
                        "Expected ts of interp to be monotonically increasing, but it was not".to_string()
                            .into(),
                    ));
                }
                prev = value;
                ts_vec.push(value);
            }
            None => {
                return Err(PolarsError::ComputeError(
                    "Expected ts of interp to not contain null values, but it contains at least one null value".to_string().into(),
                ))
            }
        }
    }

    let mut result = Vec::with_capacity(t.len());

    for maybe_t in t {
        let Some(t) = maybe_t else {
            result.push(None);
            continue;
        };

        if t.is_nan() {
            result.push(Some(t));
            continue;
        }

        match ts_vec.binary_search_by(|probe| probe.partial_cmp(&t).unwrap()) {
            Ok(i) => {
                result.push(ys.get(i));
                continue;
            }
            Err(i) => {
                if i == 0 || i == ts_vec.len() {
                    // Happens only when t is outside the range of ts
                    result.push(None);
                    continue;
                }

                let t0 = ts_vec[i - 1];
                let t1 = ts_vec[i];

                match (ys.get(i - 1), ys.get(i)) {
                    (Some(y0), Some(y1)) => {
                        result.push(Some(y0 + (y1 - y0) / (t1 - t0) * (t - t0)));
                    }
                    _ => result.push(None),
                }
            }
        }
    }

    Ok(Column::new("".into(), result))
}

#[derive(Debug, Clone, PartialEq)]
pub struct Interp {
    pub t: Arc<TypedExpression>,
    pub ts: Arc<TypedExpression>,
    pub ys: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Interp {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        let t = Arc::new(arguments[0].validate(df_type)?);
        let ts = Arc::new(arguments[1].validate(df_type)?);
        let ys = Arc::new(arguments[2].validate(df_type)?);

        let t_type = t.expression_type();
        let ts_type = ts.expression_type();
        let ys_type = ys.expression_type();

        // All arguments must be numeric
        if !t_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "interp".to_string(),
                parameter: "t".to_string(),
                expected: "numeric type".to_string(),
                actual: t_type.data_type(),
            });
        }
        if !ts_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "interp".to_string(),
                parameter: "ts".to_string(),
                expected: "numeric type".to_string(),
                actual: ts_type.data_type(),
            });
        }
        if !ys_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "interp".to_string(),
                parameter: "ys".to_string(),
                expected: "numeric type".to_string(),
                actual: ys_type.data_type(),
            });
        }

        // Result type is Float64 and preserves shape of input t
        Ok(Arc::new(Interp {
            t,
            ts,
            ys,
            expression_type: match t_type {
                ExpressionType::Scalar(_) => {
                    ExpressionType::Scalar(crate::data_type::DataType::Float64)
                }
                ExpressionType::Array(_) => {
                    ExpressionType::Array(crate::data_type::DataType::Float64)
                }
            },
        }))
    }
}

impl Function for Interp {
    fn to_polars(&self) -> Expr {
        apply_multiple(
            interpolate,
            &[
                self.t.to_polars().cast(DataType::Float64),
                self.ts.to_polars().cast(DataType::Float64),
                self.ys.to_polars().cast(DataType::Float64),
            ],
            |_, fields| Ok(fields[0].clone()),
            true,
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Interp {
            t: Arc::new(self.t.substitute(substitutions)),
            ts: Arc::new(self.ts.substitute(substitutions)),
            ys: Arc::new(self.ys.substitute(substitutions)),
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
        if let Some(other) = other.as_any().downcast_ref::<Interp>() {
            self.t == other.t
                && self.ts == other.ts
                && self.ys == other.ys
                && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "interp"
    }
}
