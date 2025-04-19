use super::Function;
use crate::expression::Expression;
use polars::prelude::*;
use std::any::Any;
use std::sync::Arc;

#[derive(Debug, Clone, PartialEq)]
pub struct Floor {
    pub argument: Arc<Expression>,
}

impl Function for Floor {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().floor()
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Floor {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Floor>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Ceil {
    pub argument: Arc<Expression>,
}

impl Function for Ceil {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().ceil()
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Ceil {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Ceil>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}
