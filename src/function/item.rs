use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};
use polars::prelude::*;
use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

#[derive(Debug, Clone, PartialEq)]
pub struct First {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl First {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "first".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        Ok(Arc::new(First {
            argument: Arc::new(typed_arg),
            expression_type: arg_type,
        }))
    }
}

impl Function for First {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().first()
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(First {
            argument: Arc::new(self.argument.substitute(substitutions)),
            expression_type: self.expression_type,
        })
    }

    fn expression_type(&self) -> ExpressionType {
        self.expression_type
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<First>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "first"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Last {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Last {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "last".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        Ok(Arc::new(Last {
            argument: Arc::new(typed_arg),
            expression_type: arg_type,
        }))
    }
}

impl Function for Last {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().last()
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Last {
            argument: Arc::new(self.argument.substitute(substitutions)),
            expression_type: self.expression_type,
        })
    }

    fn expression_type(&self) -> ExpressionType {
        self.expression_type
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Last>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "last"
    }
}
