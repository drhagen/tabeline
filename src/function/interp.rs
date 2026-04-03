use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    require_numeric, DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
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
        if arguments.len() != 3 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "interp".to_string(),
                expected: 3,
                actual: arguments.len(),
            });
        }

        let t = arguments[0].validate(df_type)?;
        let ts = arguments[1].validate(df_type)?;
        let ys = arguments[2].validate(df_type)?;

        let t_type = t.expression_type();
        let ts_type = ts.expression_type();
        let ys_type = ys.expression_type();

        require_numeric(t_type, "interp", "t")?;
        require_numeric(ts_type, "interp", "ts")?;
        require_numeric(ys_type, "interp", "ys")?;

        let float64 = crate::data_type::DataType::Float64;
        let nothing = crate::data_type::DataType::Nothing;
        let result_type = if t_type.data_type() == nothing
            || ts_type.data_type() == nothing
            || ys_type.data_type() == nothing
        {
            t_type.with_data_type(nothing)
        } else {
            t_type.with_data_type(float64)
        };

        Ok(Arc::new(Interp {
            t: Arc::new(t.cast_if_needed(float64)),
            ts: Arc::new(ts.cast_if_needed(float64)),
            ys: Arc::new(ys.cast_if_needed(float64)),
            expression_type: result_type,
        }))
    }
}

impl Function for Interp {
    fn to_polars(&self) -> Expr {
        if self.expression_type.data_type() == crate::data_type::DataType::Nothing {
            lit(NULL)
        } else {
            apply_multiple(
                interpolate,
                &[self.t.to_polars(), self.ts.to_polars(), self.ys.to_polars()],
                |_, fields| Ok(fields[0].clone()),
                true,
            )
        }
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
