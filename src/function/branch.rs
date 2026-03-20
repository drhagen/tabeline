use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    harmonize_expression_types, require_boolean, DataFrameType, ExpressionType, Function,
    TypedExpression, ValidationError,
};

#[derive(Debug, Clone, PartialEq)]
pub struct IfElse {
    pub condition: Arc<TypedExpression>,
    pub then_branch: Arc<TypedExpression>,
    pub else_branch: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl IfElse {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() < 2 || arguments.len() > 3 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "if_else".to_string(),
                expected: 2,
                actual: arguments.len(),
            });
        }

        let condition = arguments[0].validate(df_type)?;
        let then_branch = arguments[1].validate(df_type)?;
        let else_branch = if arguments.len() == 3 {
            arguments[2].validate(df_type)?
        } else {
            TypedExpression::NullLiteral
        };

        let condition_type = condition.expression_type();
        let then_type = then_branch.expression_type();
        let else_type = else_branch.expression_type();

        require_boolean(condition_type, "if_else", "condition")?;

        let result_type = harmonize_expression_types(then_type, else_type, "if_else")?;

        // If condition is Array, result must be Array regardless of branch shapes
        let result_type = if !condition_type.is_scalar() {
            ExpressionType::Array(result_type.data_type())
        } else {
            result_type
        };

        // Cast branches to promoted type
        let result_dt = result_type.data_type();
        let then_branch = then_branch.cast_if_needed(result_dt);
        let else_branch = else_branch.cast_if_needed(result_dt);

        Ok(Arc::new(IfElse {
            condition: Arc::new(condition),
            then_branch: Arc::new(then_branch),
            else_branch: Arc::new(else_branch),
            expression_type: result_type,
        }))
    }
}

impl Function for IfElse {
    fn to_polars(&self) -> Expr {
        ternary_expr(
            self.condition.to_polars(),
            self.then_branch.to_polars(),
            self.else_branch.to_polars(),
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(IfElse {
            condition: Arc::new(self.condition.substitute(substitutions)),
            then_branch: Arc::new(self.then_branch.substitute(substitutions)),
            else_branch: Arc::new(self.else_branch.substitute(substitutions)),
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
        if let Some(other) = other.as_any().downcast_ref::<IfElse>() {
            self.condition == other.condition
                && self.then_branch == other.then_branch
                && self.else_branch == other.else_branch
                && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "if_else"
    }
}
