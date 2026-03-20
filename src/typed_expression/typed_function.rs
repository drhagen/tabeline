use crate::typed_expression::{ExpressionType, TypedExpression};
use polars::prelude::Expr;
use std::collections::HashMap;
use std::fmt::Debug;
use std::sync::Arc;

pub trait Function: Debug + Sync + Send {
    fn to_polars(&self) -> Expr;

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function>;

    fn expression_type(&self) -> ExpressionType;

    fn as_any(&self) -> &dyn std::any::Any;

    fn equals(&self, other: &dyn Function) -> bool;

    fn name(&self) -> &'static str;
}

impl PartialEq for dyn Function {
    fn eq(&self, other: &Self) -> bool {
        self.equals(other)
    }
}
