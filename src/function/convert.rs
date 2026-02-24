use crate::data_type::DataType;
use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};
use polars::datatypes::DataType as PolarsDataType;
use polars::prelude::*;
use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

#[derive(Debug, Clone, PartialEq)]
pub struct ToBoolean {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl ToBoolean {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "to_boolean".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        Ok(Arc::new(ToBoolean {
            argument: Arc::new(typed_arg),
            expression_type: match arg_type {
                ExpressionType::Scalar(_) => ExpressionType::Scalar(DataType::Boolean),
                ExpressionType::Array(_) => ExpressionType::Array(DataType::Boolean),
            },
        }))
    }
}

impl Function for ToBoolean {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().cast(PolarsDataType::Boolean)
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(ToBoolean {
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
        if let Some(other) = other.as_any().downcast_ref::<ToBoolean>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "to_boolean"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ToInteger {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl ToInteger {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "to_integer".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        Ok(Arc::new(ToInteger {
            argument: Arc::new(typed_arg),
            expression_type: match arg_type {
                ExpressionType::Scalar(_) => ExpressionType::Scalar(DataType::Integer64),
                ExpressionType::Array(_) => ExpressionType::Array(DataType::Integer64),
            },
        }))
    }
}

impl Function for ToInteger {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().cast(PolarsDataType::Int64)
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(ToInteger {
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
        if let Some(other) = other.as_any().downcast_ref::<ToInteger>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "to_integer"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ToFloat {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl ToFloat {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "to_float".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        Ok(Arc::new(ToFloat {
            argument: Arc::new(typed_arg),
            expression_type: match arg_type {
                ExpressionType::Scalar(_) => ExpressionType::Scalar(DataType::Float64),
                ExpressionType::Array(_) => ExpressionType::Array(DataType::Float64),
            },
        }))
    }
}

impl Function for ToFloat {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().cast(PolarsDataType::Float64)
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(ToFloat {
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
        if let Some(other) = other.as_any().downcast_ref::<ToFloat>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "to_float"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ToString {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl ToString {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "to_string".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        Ok(Arc::new(ToString {
            argument: Arc::new(typed_arg),
            expression_type: match arg_type {
                ExpressionType::Scalar(_) => ExpressionType::Scalar(DataType::String),
                ExpressionType::Array(_) => ExpressionType::Array(DataType::String),
            },
        }))
    }
}

impl Function for ToString {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().cast(PolarsDataType::String)
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(ToString {
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
        if let Some(other) = other.as_any().downcast_ref::<ToString>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "to_string"
    }
}
