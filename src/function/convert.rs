use super::Function;
use crate::expression::Expression;
use polars::datatypes::DataType;
use polars::prelude::*;
use std::any::Any;
use std::sync::Arc;

#[derive(Debug, Clone, PartialEq)]
pub struct ToBoolean {
    pub argument: Arc<Expression>,
}

impl Function for ToBoolean {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().cast(DataType::Boolean)
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(ToBoolean {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<ToBoolean>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ToInteger {
    pub argument: Arc<Expression>,
}

impl Function for ToInteger {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().cast(DataType::Int64)
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(ToInteger {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<ToInteger>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ToFloat {
    pub argument: Arc<Expression>,
}

impl Function for ToFloat {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().cast(DataType::Float64)
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(ToFloat {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<ToFloat>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ToString {
    pub argument: Arc<Expression>,
}

impl Function for ToString {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().cast(DataType::String)
    }

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(ToString {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<ToString>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}
