use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc as StdArc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};

#[derive(Debug, Clone, PartialEq)]
pub struct RowIndex0 {
    pub expression_type: ExpressionType,
}

impl RowIndex0 {
    pub fn validate(
        arguments: Vec<StdArc<Expression>>,
        _df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if !arguments.is_empty() {
            return Err(ValidationError::FunctionArgumentCount {
                function: "row_index0".to_string(),
                expected: 0,
                actual: arguments.len(),
            });
        }

        Ok(Arc::new(RowIndex0 {
            expression_type: ExpressionType::Array(crate::data_type::DataType::Integer64),
        }))
    }
}

impl Function for RowIndex0 {
    fn to_polars(&self) -> Expr {
        int_range(Expr::from(0i64), len(), 1, polars::prelude::DataType::Int64)
    }

    fn substitute(&self, _substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(RowIndex0 {
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
        if let Some(other) = other.as_any().downcast_ref::<RowIndex0>() {
            self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "row_index_0"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct RowIndex1 {
    pub expression_type: ExpressionType,
}

impl RowIndex1 {
    pub fn validate(
        arguments: Vec<StdArc<Expression>>,
        _df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if !arguments.is_empty() {
            return Err(ValidationError::FunctionArgumentCount {
                function: "row_index1".to_string(),
                expected: 0,
                actual: arguments.len(),
            });
        }

        Ok(Arc::new(RowIndex1 {
            expression_type: ExpressionType::Array(crate::data_type::DataType::Integer64),
        }))
    }
}

impl Function for RowIndex1 {
    fn to_polars(&self) -> Expr {
        int_range(
            Expr::from(0i64),
            len() + Expr::from(1i64),
            1,
            polars::prelude::DataType::Int64,
        )
    }

    fn substitute(&self, _substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(RowIndex1 {
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
        if let Some(other) = other.as_any().downcast_ref::<RowIndex1>() {
            self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "row_index_1"
    }
}
