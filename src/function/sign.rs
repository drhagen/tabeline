use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, TypedExpression, Function, ValidationError,
};
use polars::prelude::*;
use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

#[derive(Debug, Clone, PartialEq)]
pub struct Abs {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Abs {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "abs".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "abs".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        Ok(Arc::new(Abs {
            argument: Arc::new(typed_arg),
            expression_type: arg_type,
        }))
    }
}

impl Function for Abs {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().abs()
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Abs {
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
        if let Some(other) = other.as_any().downcast_ref::<Abs>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "abs"
    }
}
