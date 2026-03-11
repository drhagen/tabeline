use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};

#[derive(Debug, Clone, PartialEq)]
pub struct Max {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Max {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "max".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "max".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        if !arg_type.is_array() {
            return Err(ValidationError::FunctionArgumentType {
                function: "max".to_string(),
                parameter: "argument".to_string(),
                expected: "array type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        Ok(Arc::new(Max {
            argument: Arc::new(typed_arg),
            expression_type: ExpressionType::Scalar(arg_type.data_type()),
        }))
    }
}

impl Function for Max {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().max()
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Max {
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
        if let Some(other) = other.as_any().downcast_ref::<Max>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "max"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Min {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Min {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "min".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "min".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        if !arg_type.is_array() {
            return Err(ValidationError::FunctionArgumentType {
                function: "min".to_string(),
                parameter: "argument".to_string(),
                expected: "array type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        Ok(Arc::new(Min {
            argument: Arc::new(typed_arg),
            expression_type: ExpressionType::Scalar(arg_type.data_type()),
        }))
    }
}

impl Function for Min {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().min()
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Min {
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
        if let Some(other) = other.as_any().downcast_ref::<Min>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "min"
    }
}
