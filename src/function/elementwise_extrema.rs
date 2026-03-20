use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::lazy::dsl::max_horizontal;
use polars::lazy::dsl::min_horizontal;
use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    require_numeric, DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};

#[derive(Debug, Clone, PartialEq)]
pub struct PMax {
    pub arguments: Vec<Arc<TypedExpression>>,
    pub expression_type: ExpressionType,
}

impl PMax {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.is_empty() {
            return Err(ValidationError::FunctionArgumentCount {
                function: "pmax".to_string(),
                expected: 1,
                actual: 0,
            });
        }

        let mut typed_args = Vec::new();
        let mut result_type: Option<ExpressionType> = None;

        for arg in arguments {
            let typed_arg = arg.validate(df_type)?;
            let arg_type = typed_arg.expression_type();

            require_numeric(arg_type, "pmax", "argument")?;

            result_type = Some(match result_type {
                None => arg_type,
                Some(rt) => {
                    crate::typed_expression::promote_expression_types(rt, arg_type, "pmax")?
                }
            });

            typed_args.push(typed_arg);
        }

        let result_type = result_type.unwrap();
        let result_dt = result_type.data_type();
        let typed_args = typed_args
            .into_iter()
            .map(|arg| Arc::new(arg.cast_if_needed(result_dt)))
            .collect();

        Ok(Arc::new(PMax {
            arguments: typed_args,
            expression_type: result_type,
        }) as Arc<dyn Function>)
    }
}

impl Function for PMax {
    fn to_polars(&self) -> Expr {
        if self.arguments.len() == 1 {
            return self.arguments[0].to_polars();
        }

        let exprs: Vec<Expr> = self.arguments.iter().map(|arg| arg.to_polars()).collect();

        let max_val = max_horizontal(&exprs).expect("pmax requires at least one argument");

        let any_null = exprs
            .iter()
            .map(|e| e.clone().is_null())
            .reduce(|acc, e| acc.or(e))
            .unwrap();

        when(any_null).then(lit(NULL)).otherwise(max_val)
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(PMax {
            arguments: self
                .arguments
                .iter()
                .map(|arg| Arc::new(arg.substitute(substitutions)))
                .collect(),
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
        if let Some(other) = other.as_any().downcast_ref::<PMax>() {
            self.arguments == other.arguments && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "pmax"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct PMin {
    pub arguments: Vec<Arc<TypedExpression>>,
    pub expression_type: ExpressionType,
}

impl PMin {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.is_empty() {
            return Err(ValidationError::FunctionArgumentCount {
                function: "pmin".to_string(),
                expected: 1,
                actual: 0,
            });
        }

        let mut typed_args = Vec::new();
        let mut result_type: Option<ExpressionType> = None;

        for arg in arguments {
            let typed_arg = arg.validate(df_type)?;
            let arg_type = typed_arg.expression_type();

            require_numeric(arg_type, "pmin", "argument")?;

            result_type = Some(match result_type {
                None => arg_type,
                Some(rt) => {
                    crate::typed_expression::promote_expression_types(rt, arg_type, "pmin")?
                }
            });

            typed_args.push(typed_arg);
        }

        let result_type = result_type.unwrap();
        let result_dt = result_type.data_type();
        let typed_args = typed_args
            .into_iter()
            .map(|arg| Arc::new(arg.cast_if_needed(result_dt)))
            .collect();

        Ok(Arc::new(PMin {
            arguments: typed_args,
            expression_type: result_type,
        }) as Arc<dyn Function>)
    }
}

impl Function for PMin {
    fn to_polars(&self) -> Expr {
        if self.arguments.len() == 1 {
            return self.arguments[0].to_polars();
        }

        let exprs: Vec<Expr> = self.arguments.iter().map(|arg| arg.to_polars()).collect();

        let min_val = min_horizontal(&exprs).expect("pmin requires at least one argument");

        let any_null = exprs
            .iter()
            .map(|e| e.clone().is_null())
            .reduce(|acc, e| acc.or(e))
            .unwrap();

        when(any_null).then(lit(NULL)).otherwise(min_val)
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(PMin {
            arguments: self
                .arguments
                .iter()
                .map(|arg| Arc::new(arg.substitute(substitutions)))
                .collect(),
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
        if let Some(other) = other.as_any().downcast_ref::<PMin>() {
            self.arguments == other.arguments && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "pmin"
    }
}
