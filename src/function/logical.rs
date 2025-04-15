use super::Function;
use crate::expression::Expression;
use polars::prelude::*;
use std::sync::Arc;

#[derive(Debug, Clone, PartialEq)]
pub struct Any {
    pub argument: Arc<Expression>,
}

impl Function for Any {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().any(false)
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Any {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn std::any::Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Any>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct All {
    pub argument: Arc<Expression>,
}

impl Function for All {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().all(false)
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(All {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn std::any::Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<All>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}
