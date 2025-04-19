use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use super::Function;
use crate::expression::Expression;

#[derive(Debug, Clone, PartialEq)]
pub struct Max {
    pub argument: Arc<Expression>,
}

impl Function for Max {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().max()
    }

    fn substitute(&self, substitutions: &HashMap<&str, Expression>) -> Box<dyn Function> {
        Box::new(Max {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Max>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Min {
    pub argument: Arc<Expression>,
}

impl Function for Min {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().min()
    }

    fn substitute(&self, substitutions: &HashMap<&str, Expression>) -> Box<dyn Function> {
        Box::new(Min {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Min>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}
