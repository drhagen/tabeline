use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    promote_expression_types, require_numeric, DataFrameType, ExpressionType, LiteralType,
    Function, TypedExpression, ValidationError,
};

#[derive(Debug, Clone, PartialEq)]
pub struct Sqrt {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Sqrt {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "sqrt".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        require_numeric(arg_type, "sqrt", "argument")?;

        let result_type = arg_type.to_float();
        let cast_arg = typed_arg.cast_if_needed(result_type.data_type());
        Ok(Arc::new(Sqrt {
            argument: Arc::new(cast_arg),
            expression_type: result_type,
        }))
    }
}

impl Function for Sqrt {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().sqrt()
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Sqrt {
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
        if let Some(other) = other.as_any().downcast_ref::<Sqrt>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "sqrt"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Exp {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Exp {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "exp".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        require_numeric(arg_type, "exp", "argument")?;

        let result_type = arg_type.to_float();
        let cast_arg = typed_arg.cast_if_needed(result_type.data_type());
        Ok(Arc::new(Exp {
            argument: Arc::new(cast_arg),
            expression_type: result_type,
        }))
    }
}

impl Function for Exp {
    fn to_polars(&self) -> Expr {
        self.argument.to_polars().exp()
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Exp {
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
        if let Some(other) = other.as_any().downcast_ref::<Exp>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "exp"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Pow {
    pub base: Arc<TypedExpression>,
    pub exponent: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Pow {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 2 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "pow".to_string(),
                expected: 2,
                actual: arguments.len(),
            });
        }

        let typed_base = arguments[0].validate(df_type)?;
        let typed_exponent = arguments[1].validate(df_type)?;

        let base_type = typed_base.expression_type();
        let exponent_type = typed_exponent.expression_type();

        require_numeric(base_type, "pow", "base")?;
        require_numeric(exponent_type, "pow", "exponent")?;

        let promoted_type =
            promote_expression_types(base_type, exponent_type, "pow")?;

        // Check wholeness on the original exponent type, before any casting
        let exponent_is_whole = match exponent_type {
            ExpressionType::Literal(LiteralType::Whole(_)) => true,
            ExpressionType::Literal(_) => false,
            _ => exponent_type.data_type().is_whole(),
        };

        let expression_type = if exponent_is_whole {
            // anything ** whole → preserves base type
            let base_dt = if base_type.is_literal() || exponent_type.is_literal() {
                promoted_type.data_type()
            } else {
                base_type.data_type()
            };
            promoted_type.with_data_type(base_dt)
        } else {
            // anything ** int/float → float operation
            let result_dt = promoted_type.data_type();
            let float_dt = result_dt.promote_to_float(result_dt);
            promoted_type.with_data_type(float_dt)
        };

        let result_dt = expression_type.data_type();
        Ok(Arc::new(Pow {
            base: Arc::new(typed_base.cast_if_needed(result_dt)),
            exponent: Arc::new(typed_exponent.cast_if_needed(result_dt)),
            expression_type,
        }))
    }
}

impl Function for Pow {
    fn to_polars(&self) -> Expr {
        self.base.to_polars().pow(self.exponent.to_polars())
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Pow {
            base: Arc::new(self.base.substitute(substitutions)),
            exponent: Arc::new(self.exponent.substitute(substitutions)),
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
        if let Some(other) = other.as_any().downcast_ref::<Pow>() {
            self.base == other.base
                && self.exponent == other.exponent
                && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "pow"
    }
}
