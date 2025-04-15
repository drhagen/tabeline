use std::any::Any;
use std::sync::Arc;

use polars::prelude::*;

use super::Function;
use crate::expression::Expression;

#[derive(Debug, Clone, PartialEq)]
pub struct Sqrt {
    pub argument: Arc<Expression>,
}

impl Function for Sqrt {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().sqrt()
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Sqrt {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Sqrt>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Exp {
    pub argument: Arc<Expression>,
}

impl Function for Exp {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().exp()
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Exp {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Exp>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Pow {
    pub base: Arc<Expression>,
    pub exponent: Arc<Expression>,
}

impl Function for Pow {
    fn to_polars(&self) -> Expr {
        self.base.to_polars().pow(self.exponent.to_polars())
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Pow {
            base: Arc::new(self.base.substitute(substitutions)),
            exponent: Arc::new(self.exponent.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Pow>() {
            self.base == other.base && self.exponent == other.exponent
        } else {
            false
        }
    }
}
