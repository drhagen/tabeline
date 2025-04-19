use super::Function;
use crate::expression::Expression;
use polars::prelude::*;
use std::any::Any;
use std::sync::Arc;

#[derive(Debug, Clone, PartialEq)]
pub struct Abs {
    pub argument: Arc<Expression>,
}

impl Function for Abs {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().abs()
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Abs {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Abs>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}
