use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::lazy::dsl::max_horizontal;
use polars::lazy::dsl::min_horizontal;
use polars::prelude::*;

use super::Function;
use crate::expression::Expression;

#[derive(Debug, Clone, PartialEq)]
pub struct PMax {
    pub arguments: Vec<Arc<Expression>>,
}

impl Function for PMax {
    fn to_polars(&self) -> Expr {
        if self.arguments.len() == 1 {
            return self.arguments[0].to_polars();
        }

        let exprs: Vec<Expr> = self.arguments.iter().map(|arg| arg.to_polars()).collect();

        // max_horizontal returns an error if exprs is empty
        let max_val = max_horizontal(&exprs).expect("pmax requires at least one argument");

        // Check if any value is null, if so return null, otherwise return max
        let any_null = exprs
            .iter()
            .map(|e| e.clone().is_null())
            .reduce(|acc, e| acc.or(e))
            .unwrap();

        when(any_null).then(lit(NULL)).otherwise(max_val)
    }

    fn substitute(&self, substitutions: &HashMap<&str, Expression>) -> Box<dyn Function> {
        Box::new(PMax {
            arguments: self
                .arguments
                .iter()
                .map(|arg| Arc::new(arg.substitute(substitutions)))
                .collect(),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<PMax>() {
            self.arguments == other.arguments
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct PMin {
    pub arguments: Vec<Arc<Expression>>,
}

impl Function for PMin {
    fn to_polars(&self) -> Expr {
        if self.arguments.len() == 1 {
            return self.arguments[0].to_polars();
        }

        let exprs: Vec<Expr> = self.arguments.iter().map(|arg| arg.to_polars()).collect();

        // min_horizontal returns an error if exprs is empty
        let min_val = min_horizontal(&exprs).expect("pmin requires at least one argument");

        // Check if any value is null, if so return null, otherwise return min
        let any_null = exprs
            .iter()
            .map(|e| e.clone().is_null())
            .reduce(|acc, e| acc.or(e))
            .unwrap();

        when(any_null).then(lit(NULL)).otherwise(min_val)
    }

    fn substitute(&self, substitutions: &HashMap<&str, Expression>) -> Box<dyn Function> {
        Box::new(PMin {
            arguments: self
                .arguments
                .iter()
                .map(|arg| Arc::new(arg.substitute(substitutions)))
                .collect(),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<PMin>() {
            self.arguments == other.arguments
        } else {
            false
        }
    }
}
