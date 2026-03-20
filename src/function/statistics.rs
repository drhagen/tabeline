use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    require_array, require_numeric, DataFrameType, ExpressionType, Function, TypedExpression,
    ValidationError,
};

#[derive(Debug, Clone, PartialEq)]
pub struct Std {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Std {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "std".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let argument = arguments[0].validate(df_type)?;
        let arg_type = argument.expression_type();

        require_numeric(arg_type, "std", "argument")?;
        require_array(arg_type, "std", "argument")?;

        let result_dt = arg_type.data_type().to_float();
        Ok(Arc::new(Std {
            argument: Arc::new(argument.cast_if_needed(result_dt)),
            expression_type: ExpressionType::Scalar(result_dt),
        }))
    }
}

impl Function for Std {
    fn to_polars(&self) -> Expr {
        let polars_expression = self.argument.to_polars();
        ternary_expr(
            polars_expression.clone().is_null().any(false),
            lit(NULL),
            polars_expression.std(1),
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Std {
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
        if let Some(other) = other.as_any().downcast_ref::<Std>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "std"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Var {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Var {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "var".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let argument = arguments[0].validate(df_type)?;
        let arg_type = argument.expression_type();

        require_numeric(arg_type, "var", "argument")?;
        require_array(arg_type, "var", "argument")?;

        let result_dt = arg_type.data_type().to_float();
        Ok(Arc::new(Var {
            argument: Arc::new(argument.cast_if_needed(result_dt)),
            expression_type: ExpressionType::Scalar(result_dt),
        }))
    }
}

impl Function for Var {
    fn to_polars(&self) -> Expr {
        let polars_expression = self.argument.to_polars();
        ternary_expr(
            polars_expression.clone().is_null().any(false),
            lit(NULL),
            polars_expression.var(1),
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Var {
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
        if let Some(other) = other.as_any().downcast_ref::<Var>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "var"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Sum {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Sum {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "sum".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let argument = arguments[0].validate(df_type)?;
        let arg_type = argument.expression_type();

        require_numeric(arg_type, "sum", "argument")?;
        require_array(arg_type, "sum", "argument")?;

        Ok(Arc::new(Sum {
            argument: Arc::new(argument),
            expression_type: ExpressionType::Scalar(arg_type.data_type()),
        }))
    }
}

impl Function for Sum {
    fn to_polars(&self) -> Expr {
        let polars_expression = self.argument.to_polars();
        ternary_expr(
            polars_expression.clone().is_null().any(false),
            lit(NULL),
            polars_expression.sum(),
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Sum {
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
        if let Some(other) = other.as_any().downcast_ref::<Sum>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "sum"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Mean {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Mean {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "mean".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let argument = arguments[0].validate(df_type)?;
        let arg_type = argument.expression_type();

        require_numeric(arg_type, "mean", "argument")?;
        require_array(arg_type, "mean", "argument")?;

        let result_dt = arg_type.data_type().to_float();
        Ok(Arc::new(Mean {
            argument: Arc::new(argument.cast_if_needed(result_dt)),
            expression_type: ExpressionType::Scalar(result_dt),
        }))
    }
}

impl Function for Mean {
    fn to_polars(&self) -> Expr {
        let polars_expression = self.argument.to_polars();
        ternary_expr(
            polars_expression.clone().is_null().any(false),
            lit(NULL),
            polars_expression.mean(),
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Mean {
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
        if let Some(other) = other.as_any().downcast_ref::<Mean>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "mean"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Median {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Median {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 1 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "median".to_string(),
                expected: 1,
                actual: arguments.len(),
            });
        }

        let argument = arguments[0].validate(df_type)?;
        let arg_type = argument.expression_type();

        require_numeric(arg_type, "median", "argument")?;
        require_array(arg_type, "median", "argument")?;

        let result_dt = arg_type.data_type().to_float();
        Ok(Arc::new(Median {
            argument: Arc::new(argument.cast_if_needed(result_dt)),
            expression_type: ExpressionType::Scalar(result_dt),
        }))
    }
}

impl Function for Median {
    fn to_polars(&self) -> Expr {
        let polars_expression = self.argument.to_polars();
        ternary_expr(
            polars_expression.clone().is_null().any(false),
            lit(NULL),
            polars_expression.median(),
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Median {
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
        if let Some(other) = other.as_any().downcast_ref::<Median>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "median"
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Quantile {
    pub argument: Arc<TypedExpression>,
    pub quantile: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Quantile {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        if arguments.len() != 2 {
            return Err(ValidationError::FunctionArgumentCount {
                function: "quantile".to_string(),
                expected: 2,
                actual: arguments.len(),
            });
        }

        let argument = arguments[0].validate(df_type)?;
        let quantile = arguments[1].validate(df_type)?;

        let arg_type = argument.expression_type();
        let quantile_type = quantile.expression_type();

        require_numeric(arg_type, "quantile", "argument")?;
        require_array(arg_type, "quantile", "argument")?;
        require_numeric(quantile_type, "quantile", "quantile")?;

        let result_dt = arg_type.data_type().to_float();
        Ok(Arc::new(Quantile {
            argument: Arc::new(argument.cast_if_needed(result_dt)),
            quantile: Arc::new(quantile.cast_if_needed(result_dt)),
            expression_type: ExpressionType::Scalar(result_dt),
        }))
    }
}

impl Function for Quantile {
    fn to_polars(&self) -> Expr {
        let polars_expression = self.argument.to_polars();
        ternary_expr(
            polars_expression.clone().is_null().any(false),
            lit(NULL),
            polars_expression.quantile(self.quantile.to_polars(), QuantileMethod::Linear),
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Quantile {
            argument: Arc::new(self.argument.substitute(substitutions)),
            quantile: Arc::new(self.quantile.substitute(substitutions)),
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
        if let Some(other) = other.as_any().downcast_ref::<Quantile>() {
            self.argument == other.argument
                && self.quantile == other.quantile
                && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "quantile"
    }
}
