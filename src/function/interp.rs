use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use super::Function;
use crate::expression::Expression;

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
    pub t: Arc<Expression>,
    pub ts: Arc<Expression>,
    pub ys: Arc<Expression>,
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

    fn substitute(&self, substitutions: &HashMap<&str, Expression>) -> Box<dyn Function> {
        Box::new(Interp {
            t: Arc::new(self.t.substitute(substitutions)),
            ts: Arc::new(self.ts.substitute(substitutions)),
            ys: Arc::new(self.ys.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Interp>() {
            self.t == other.t && self.ts == other.ts && self.ys == other.ys
        } else {
            false
        }
    }
}
