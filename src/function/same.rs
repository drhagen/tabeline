use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use super::Function;
use crate::expression::Expression;

fn same(column: Column) -> PolarsResult<Option<Column>> {
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

        Ok(Some(col))
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
        self.argument
            .to_polars()
            .apply(same, Default::default())
            // WORKAROUND: Use first instead of FunctionFlags::RETURNS_SCALAR
            // because that is broken when returning a null
            // https://github.com/pola-rs/polars/issues/20679
            .first()
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
