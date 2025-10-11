use std::any::Any;
use std::f64::consts::E;
use std::sync::Arc;

use polars::prelude::*;

use super::Function;
use crate::expression::Expression;

#[derive(Debug, Clone, PartialEq)]
pub struct Log {
    pub argument: Arc<Expression>,
}

impl Function for Log {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().log(Expr::from(E))
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Log {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Log>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Log2 {
    pub argument: Arc<Expression>,
}

impl Function for Log2 {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().log(Expr::from(2.0))
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Log2 {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Log2>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Log10 {
    pub argument: Arc<Expression>,
}

impl Function for Log10 {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().log(Expr::from(10.0))
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Log10 {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Log10>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}
