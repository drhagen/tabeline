use super::Function;
use crate::expression::Expression;
use polars::prelude::*;
use std::sync::Arc;

#[derive(Debug, Clone, PartialEq)]
pub struct First {
    pub argument: Arc<Expression>,
}

impl Function for First {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().first()
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(First {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn std::any::Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<First>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Last {
    pub argument: Arc<Expression>,
}

impl Function for Last {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().last()
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Last {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn std::any::Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Last>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}
