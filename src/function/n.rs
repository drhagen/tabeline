use std::{any::Any, collections::HashMap};

use polars::prelude::*;

use crate::expression::Expression;

use super::Function;

#[derive(Debug, Clone, PartialEq)]
pub struct N {}

impl Function for N {
    fn to_polars(&self) -> Expr {
        len()
    }

    fn substitute(&self, _substitutions: &HashMap<&str, Expression>) -> Box<dyn Function> {
        Box::new(N {})
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        matches!(other.as_any().downcast_ref::<N>(), Some(_other))
    }
}
