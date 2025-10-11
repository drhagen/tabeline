use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use super::Function;
use crate::expression::Expression;

fn same(args: &mut [Column]) -> PolarsResult<Column> {
    let column = &args[0];

    if column.n_unique()? == 1 {
        let val = match column.get(0) {
            Ok(value) => value.into_static(),
            Err(_) => {
                return Err(PolarsError::ComputeError(
                    "Expected a non-empty column for same, but got empty".into(),
                ))
            }
        };

        let col = Column::new_scalar("".into(), Scalar::new(column.dtype().clone(), val), 1);

        Ok(col)
    } else {
        let unique_elements = column.unique()?;
        Err(PolarsError::ComputeError(
            format!(
                "Expected all elements to be the same, but got {} unique elements: {:?}",
                unique_elements.len(),
                unique_elements
            )
            .into(),
        ))
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Same {
    pub argument: Arc<Expression>,
}

impl Function for Same {
    fn to_polars(&self) -> Expr {
        // Use apply_multiple because it is the only function that accepts returns_scalar
        apply_multiple(
            same,
            &[self.argument.to_polars()],
            |_, fields| Ok(fields[0].clone()),
            true,
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, Expression>) -> Box<dyn Function> {
        Box::new(Same {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Same>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}
