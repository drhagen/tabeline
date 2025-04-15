use std::any::Any;
use std::sync::Arc;

use polars::prelude::*;

use super::Function;
use crate::expression::Expression;

#[derive(Debug, Clone, PartialEq)]
pub struct Std {
    pub argument: Arc<Expression>,
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

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Std {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Std>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Var {
    pub argument: Arc<Expression>,
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

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Var {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Var>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Sum {
    pub argument: Arc<Expression>,
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

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Sum {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Sum>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Mean {
    pub argument: Arc<Expression>,
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

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Mean {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Mean>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Median {
    pub argument: Arc<Expression>,
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

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Median {
            argument: Arc::new(self.argument.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Median>() {
            self.argument == other.argument
        } else {
            false
        }
    }
}
#[derive(Debug, Clone, PartialEq)]
pub struct Quantile {
    pub argument: Arc<Expression>,
    pub quantile: Arc<Expression>,
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

    fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, Expression>,
    ) -> Box<dyn Function> {
        Box::new(Quantile {
            argument: Arc::new(self.argument.substitute(substitutions)),
            quantile: Arc::new(self.quantile.substitute(substitutions)),
        })
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn equals(&self, other: &dyn Function) -> bool {
        if let Some(other) = other.as_any().downcast_ref::<Quantile>() {
            self.argument == other.argument && self.quantile == other.quantile
        } else {
            false
        }
    }
}
