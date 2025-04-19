use std::any::Any;
use std::sync::Arc;

use polars::prelude::*;

use super::Function;
use crate::expression::Expression;

#[derive(Debug, Clone, PartialEq)]
pub struct IfElse {
    pub condition: Arc<Expression>,
    pub then_branch: Arc<Expression>,
    pub else_branch: Arc<Expression>,
}

impl Function for IfElse {
    fn to_polars(&self) -> Expr {
        ternary_expr(
            self.condition.to_polars(),
            self.then_branch.to_polars(),
            self.else_branch.to_polars(),
        )
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(IfElse {
            condition: Arc::new(self.condition.substitute(substitutions)),
            then_branch: Arc::new(self.then_branch.substitute(substitutions)),
            else_branch: Arc::new(self.else_branch.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<IfElse>() {
            self.condition == other.condition
                && self.then_branch == other.then_branch
                && self.else_branch == other.else_branch
        } else {
            false
        }
    }
}
