use crate::expression::Expression;
use crate::typed_expression::{
    require_array, require_boolean, DataFrameType, ExpressionType, Function, TypedExpression,
    ValidationError,
};
use polars::prelude::*;
use std::any::Any as StdAny;
use std::collections::HashMap;
use std::sync::Arc;

#[derive(Debug, Clone, PartialEq)]
pub struct Any {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Any {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "any".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        require_boolean(arg_type, "any", "argument")?;
        require_array(arg_type, "any", "argument")?;

        Ok(Arc::new(Any {
            argument: Arc::new(typed_arg),
            expression_type: ExpressionType::Scalar(arg_type.data_type()),
        }))
    }
}

impl Function for Any {
    fn to_polars(&self) -> Expr {
        if self.argument.expression_type().data_type() == crate::data_type::DataType::Nothing {
            // WORKAROUND: Polars any() crashes on DataType::Null (Nothing) columns;
            // any(nothing) = nothing per three-value logic
            lit(NULL)
        } else {
            self.argument.to_polars().any(false)
        }
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Any {
            argument: Arc::new(self.argument.substitute(substitutions)),
            expression_type: self.expression_type,
        })
    }

    fn expression_type(&self) -> ExpressionType {
        self.expression_type
    }

    fn as_any(&self) -> &dyn StdAny {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Any>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "any"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct All {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl All {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "all".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        require_boolean(arg_type, "all", "argument")?;
        require_array(arg_type, "all", "argument")?;

        Ok(Arc::new(All {
            argument: Arc::new(typed_arg),
            expression_type: ExpressionType::Scalar(arg_type.data_type()),
        }))
    }
}

impl Function for All {
    fn to_polars(&self) -> Expr {
        if self.argument.expression_type().data_type() == crate::data_type::DataType::Nothing {
            // WORKAROUND: Polars all() crashes on DataType::Null (Nothing) columns;
            // all(nothing) = nothing per three-value logic
            lit(NULL)
        } else {
            self.argument.to_polars().all(false)
        }
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(All {
            argument: Arc::new(self.argument.substitute(substitutions)),
            expression_type: self.expression_type,
        })
    }

    fn expression_type(&self) -> ExpressionType {
        self.expression_type
    }

    fn as_any(&self) -> &dyn StdAny {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<All>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "all"
    }
}
