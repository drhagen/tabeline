use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
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

        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "sqrt".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

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

        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "exp".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

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

        if !base_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "pow".to_string(),
                parameter: "base".to_string(),
                expected: "numeric type".to_string(),
                actual: base_type.data_type(),
            });
        }
        if !exponent_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "pow".to_string(),
                parameter: "exponent".to_string(),
                expected: "numeric type".to_string(),
                actual: exponent_type.data_type(),
            });
        }

        let promoted_type =
            crate::typed_expression::promote_expression_types(base_type, exponent_type, "pow")?;

        // Cast both operands to the promoted type
        let promoted_dt = promoted_type.data_type();
        let typed_base = typed_base.cast_if_needed(promoted_dt);
        let typed_exponent = typed_exponent.cast_if_needed(promoted_dt);

        // Apply power type rules: anything ** whole preserves type, otherwise float
        let exponent_dt = typed_exponent.expression_type().data_type();
        let expression_type = if exponent_dt.is_whole() {
            promoted_type
        } else {
            let float_dt = typed_base
                .expression_type()
                .data_type()
                .promote_to_float(exponent_dt);
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
