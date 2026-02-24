use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use polars::prelude::*;

use crate::expression::Expression;
use crate::typed_expression::{
    DataFrameType, ExpressionType, Function, TypedExpression, ValidationError,
};

fn same(args: &mut [Column]) -> PolarsResult<Column> {
    let column = &args[0];

    if column.n_unique()? == 1 {
        let val = match column.get(0) {
            Ok(value) => value.into_static(),
            Err(_) => {
                return Err(PolarsError::ComputeError(
                    "Expected a non-empty column for same, but got empty".into(),
                ))
            }
        };

        let col = Column::new_scalar("".into(), Scalar::new(column.dtype().clone(), val), 1);

        Ok(col)
    } else {
        let unique_elements = column.unique()?;
        Err(PolarsError::ComputeError(
            format!(
                "Expected all elements to be the same, but got {} unique elements: {:?}",
                unique_elements.len(),
                unique_elements
            )
            .into(),
        ))
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Same {
    pub argument: Arc<TypedExpression>,
    pub expression_type: ExpressionType,
}

impl Same {
    pub fn validate(
        arguments: Vec<Arc<Expression>>,
        df_type: &DataFrameType,
    ) -> Result<Arc<dyn Function>, ValidationError> {
        let typed_arg = arguments[0].validate(df_type)?;
        let arg_type = typed_arg.expression_type();

        Ok(Arc::new(Same {
            argument: Arc::new(typed_arg),
            expression_type: arg_type,
        }))
    }
}

impl Function for Same {
    fn to_polars(&self) -> Expr {
        apply_multiple(
            same,
            &[self.argument.to_polars()],
            |_, fields| Ok(fields[0].clone()),
            true,
        )
    }

    fn substitute(&self, substitutions: &HashMap<&str, TypedExpression>) -> Arc<dyn Function> {
        Arc::new(Same {
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
        if let Some(other) = other.as_any().downcast_ref::<Same>() {
            self.argument == other.argument && self.expression_type == other.expression_type
        } else {
            false
        }
    }

    fn name(&self) -> &'static str {
        "same"
    }
}
