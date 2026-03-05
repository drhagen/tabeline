use std::any::Any;
use std::collections::HashMap;
use std::f64::consts::E;
use std::sync::Arc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};

macro_rules! impl_log_function {
    ($name:ident, $fn_name:literal, $base:expr) => {
        #[derive(Debug, Clone, PartialEq)]
        pub struct $name {
            pub argument: Arc<TypedExpression>,
            pub expression_type: ExpressionType,
        }

        impl $name {
            pub fn validate(
                arguments: Vec<Arc<Expression>>,
                df_type: &DataFrameType,
            ) -> Result<Arc<dyn Function>, ValidationError> {
                if arguments.len() != 1 {
                    return Err(ValidationError::FunctionArgumentCount {
                        function: $fn_name.to_string(),
                        expected: 1,
                        actual: arguments.len(),
                    });
                }

                let typed_arg = arguments[0].validate(df_type)?;
                let arg_type = typed_arg.expression_type();

                if !arg_type.data_type().is_numeric() {
                    return Err(ValidationError::FunctionArgumentType {
                        function: $fn_name.to_string(),
                        parameter: "argument".to_string(),
                        expected: "numeric type".to_string(),
                        actual: arg_type.data_type(),
                    });
                }

                let result_type = arg_type.to_float();
                let cast_arg = typed_arg.cast_if_needed(result_type.data_type());
                Ok(Arc::new($name {
                    argument: Arc::new(cast_arg),
                    expression_type: result_type,
                }))
            }
        }

        impl Function for $name {
            fn to_polars(&self) -> Expr {
                self.argument.to_polars().log(Expr::from($base))
            }

            fn substitute(
                &self,
                substitutions: &HashMap<&str, TypedExpression>,
            ) -> Arc<dyn Function> {
                Arc::new($name {
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
                if let Some(other) = other.as_any().downcast_ref::<$name>() {
                    self.argument == other.argument && self.expression_type == other.expression_type
                } else {
                    false
                }
            }

            fn name(&self) -> &'static str {
                $fn_name
            }
        }
    };
}

impl_log_function!(Log, "log", E);
impl_log_function!(Log2, "log2", 2.0);
impl_log_function!(Log10, "log10", 10.0);
