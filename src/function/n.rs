use std::any::Any;
use std::collections::HashMap;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};
use std::sync::Arc as StdArc;

#[derive(Debug, Clone, PartialEq)]
pub struct N {
    pub expression_type: ExpressionType,
}

impl N {
    pub fn validate(
        arguments: Vec<StdArc<Expression>>,
        _df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if !arguments.is_empty() {
            return Err(ValidationError::FunctionArgumentCount {
                function: "n".to_string(),
                expected: 0,
                actual: arguments.len(),
            });
        }

        Ok(Arc::new(N {
            expression_type: ExpressionType::Scalar(crate::data_type::DataType::Whole32),
        }))
    }
}

impl Function for N {
    fn to_polars(&self) -> Expr {
        len()
    }

    fn substitute(&self, _substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(N {
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
        if let Some(other) = other.as_any().downcast_ref::<N>() {
            self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "n"
    }
}
