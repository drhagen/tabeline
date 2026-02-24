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
pub struct Std {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Std {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        let argument = Arc::new(arguments[0].validate(df_type)?);
        let arg_type = argument.expression_type();

        // Std requires numeric type
        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "std".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        // Std always returns Float64 scalar (aggregation result)
        Ok(Arc::new(Std {
            argument,
            expression_type: ExpressionType::Scalar(DataType::Float64),
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
        let argument = Arc::new(arguments[0].validate(df_type)?);
        let arg_type = argument.expression_type();

        // Var requires numeric type
        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "var".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        // Var always returns Float64 scalar (aggregation result)
        Ok(Arc::new(Var {
            argument,
            expression_type: ExpressionType::Scalar(DataType::Float64),
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
        let argument = Arc::new(arguments[0].validate(df_type)?);
        let arg_type = argument.expression_type();

        // Sum requires numeric type
        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "sum".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        Ok(Arc::new(Sum {
            argument,
            expression_type: arg_type,
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
        let argument = Arc::new(arguments[0].validate(df_type)?);
        let arg_type = argument.expression_type();

        // Mean requires numeric type
        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "mean".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        // Mean always returns Float64 scalar (aggregation result)
        Ok(Arc::new(Mean {
            argument,
            expression_type: ExpressionType::Scalar(DataType::Float64),
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
        let argument = Arc::new(arguments[0].validate(df_type)?);
        let arg_type = argument.expression_type();

        // Median requires numeric type
        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "median".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        // Median always returns Float64 scalar (aggregation result)
        Ok(Arc::new(Median {
            argument,
            expression_type: ExpressionType::Scalar(DataType::Float64),
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
        let argument = Arc::new(arguments[0].validate(df_type)?);
        let quantile = Arc::new(arguments[1].validate(df_type)?);

        let arg_type = argument.expression_type();
        let quantile_type = quantile.expression_type();

        // Argument requires numeric type
        if !arg_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "quantile".to_string(),
                parameter: "argument".to_string(),
                expected: "numeric type".to_string(),
                actual: arg_type.data_type(),
            });
        }

        // Quantile parameter should be numeric
        if !quantile_type.data_type().is_numeric() {
            return Err(ValidationError::FunctionArgumentType {
                function: "quantile".to_string(),
                parameter: "quantile".to_string(),
                expected: "numeric type".to_string(),
                actual: quantile_type.data_type(),
            });
        }

        // Quantile always returns Float64 scalar (aggregation result)
        Ok(Arc::new(Quantile {
            argument,
            quantile,
            expression_type: ExpressionType::Scalar(DataType::Float64),
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
