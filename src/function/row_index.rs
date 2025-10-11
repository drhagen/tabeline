use std::{any::Any, collections::HashMap};

use polars::prelude::*;

use crate::expression::Expression;

use super::Function;

#[derive(Debug, Clone, PartialEq)]
pub struct RowIndex0 {}

impl Function for RowIndex0 {
    fn to_polars(&self) -> Expr {
        int_range(Expr::from(0i64), len(), 1, DataType::Int64)
    }

    fn substitute(&self, _substitutions: &HashMap<&str, Expression>) -> Box<dyn Function> {
        Box::new(RowIndex0 {})
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        matches!(other.as_any().downcast_ref::<RowIndex0>(), Some(_other))
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct RowIndex1 {}

impl Function for RowIndex1 {
    fn to_polars(&self) -> Expr {
        int_range(
            Expr::from(0i64),
            len() + Expr::from(1i64),
            1,
            DataType::Int64,
        )
    }

    fn substitute(&self, _substitutions: &HashMap<&str, Expression>) -> Box<dyn Function> {
        Box::new(RowIndex1 {})
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        matches!(other.as_any().downcast_ref::<RowIndex1>(), Some(_other))
    }
}
