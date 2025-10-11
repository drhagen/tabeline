use std::any::Any;
use std::sync::Arc;

use polars::prelude::*;

use super::Function;
use crate::expression::Expression;

#[derive(Debug, Clone, PartialEq)]
pub struct Trapz {
    pub t: Arc<Expression>,
    pub y: Arc<Expression>,
}

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

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Trapz {
            t: Arc::new(self.t.substitute(substitutions)),
            y: Arc::new(self.y.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Trapz>() {
            self.t == other.t && self.y == other.y
        } else {
            false
        }
    }
}
