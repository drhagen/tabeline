use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use crate::data_type::DataType;
use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};

#[derive(Debug, Clone, PartialEq)]
pub struct IsNull {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl IsNull {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "is_null".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        Ok(Arc::new(IsNull {
            argument: Arc::new(typed_arg),
            expression_type: match arg_type {
                ExpressionType::Scalar(_) => ExpressionType::Scalar(DataType::Boolean),
                ExpressionType::Array(_) => ExpressionType::Array(DataType::Boolean),
            },
        }) as Arc<dyn Function>)
    }
}

impl Function for IsNull {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().is_null()
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(IsNull {
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
        if let Some(other) = other.as_any().downcast_ref::<IsNull>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "is_null"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct IsNan {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl IsNan {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "is_nan".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "is_nan".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        Ok(Arc::new(IsNan {
            argument: Arc::new(typed_arg),
            expression_type: match arg_type {
                ExpressionType::Scalar(_) => ExpressionType::Scalar(DataType::Boolean),
                ExpressionType::Array(_) => ExpressionType::Array(DataType::Boolean),
            },
        }) as Arc<dyn Function>)
    }
}

impl Function for IsNan {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().is_nan()
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(IsNan {
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
        if let Some(other) = other.as_any().downcast_ref::<IsNan>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "is_nan"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct IsFinite {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl IsFinite {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "is_finite".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "is_finite".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        Ok(Arc::new(IsFinite {
            argument: Arc::new(typed_arg),
            expression_type: match arg_type {
                ExpressionType::Scalar(_) => ExpressionType::Scalar(DataType::Boolean),
                ExpressionType::Array(_) => ExpressionType::Array(DataType::Boolean),
            },
        }) as Arc<dyn Function>)
    }
}

impl Function for IsFinite {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().is_finite()
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(IsFinite {
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
        if let Some(other) = other.as_any().downcast_ref::<IsFinite>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "is_finite"
    }
}
