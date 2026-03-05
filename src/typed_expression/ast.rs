use crate::data_type::DataType;
use crate::typed_expression::{ExpressionType, Function};
use std::sync::Arc;

#[derive(Debug, Clone, PartialEq)]
pub enum TypedExpression {
    // Literals have fixed types - no need to store expression_type
    NullLiteral,
    BooleanLiteral {
        value: bool,
    },
    IntegerLiteral {
        value: i64,
    },
    FloatLiteral {
        value: f64,
    },
    StringLiteral {
        value: String,
    },
    Variable {
        name: String,
        expression_type: ExpressionType,
    },
    Positive {
        content: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    Negative {
        content: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    Add {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    Subtract {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    Multiply {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    TrueDivide {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    FloorDivide {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    Mod {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    Power {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    Call {
        call: Arc<dyn Function>,
    },
    Equal {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    NotEqual {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    GreaterThanOrEqual {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    LessThanOrEqual {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    GreaterThan {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    LessThan {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    Not {
        content: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    And {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    Or {
        left: Arc<TypedExpression>,
        right: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
    Cast {
        content: Arc<TypedExpression>,
        expression_type: ExpressionType,
    },
}

impl TypedExpression {
    pub fn is_literal(&self) -> bool {
        match self {
            TypedExpression::NullLiteral
            | TypedExpression::BooleanLiteral { .. }
            | TypedExpression::IntegerLiteral { .. }
            | TypedExpression::FloatLiteral { .. }
            | TypedExpression::StringLiteral { .. } => true,
            // Negated or positive literals (e.g. -2.5 parses as Negative(FloatLiteral))
            TypedExpression::Negative { content, .. }
            | TypedExpression::Positive { content, .. } => content.is_literal(),
            _ => false,
        }
    }

    /// Returns true if this expression is a float literal (including negated float literals).
    pub fn is_float_literal(&self) -> bool {
        match self {
            TypedExpression::FloatLiteral { .. } => true,
            TypedExpression::Negative { content, .. }
            | TypedExpression::Positive { content, .. } => content.is_float_literal(),
            _ => false,
        }
    }

    pub fn cast_if_needed(self, target: DataType) -> TypedExpression {
        let current = self.expression_type();
        if current.data_type() == target {
            self
        } else {
            TypedExpression::Cast {
                content: Arc::new(self),
                expression_type: current.with_data_type(target),
            }
        }
    }

    pub fn expression_type(&self) -> ExpressionType {
        match self {
            // Literals have fixed types
            TypedExpression::NullLiteral => ExpressionType::Scalar(DataType::Nothing),
            TypedExpression::BooleanLiteral { .. } => ExpressionType::Scalar(DataType::Boolean),
            TypedExpression::IntegerLiteral { .. } => ExpressionType::Scalar(DataType::Integer64),
            TypedExpression::FloatLiteral { .. } => ExpressionType::Scalar(DataType::Float64),
            TypedExpression::StringLiteral { .. } => ExpressionType::Scalar(DataType::String),
            TypedExpression::Variable {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Positive {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Negative {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Add {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Subtract {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Multiply {
                expression_type, ..
            } => *expression_type,
            TypedExpression::TrueDivide {
                expression_type, ..
            } => *expression_type,
            TypedExpression::FloorDivide {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Mod {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Power {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Call { call } => call.expression_type(),
            TypedExpression::Equal {
                expression_type, ..
            } => *expression_type,
            TypedExpression::NotEqual {
                expression_type, ..
            } => *expression_type,
            TypedExpression::GreaterThanOrEqual {
                expression_type, ..
            } => *expression_type,
            TypedExpression::LessThanOrEqual {
                expression_type, ..
            } => *expression_type,
            TypedExpression::GreaterThan {
                expression_type, ..
            } => *expression_type,
            TypedExpression::LessThan {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Not {
                expression_type, ..
            } => *expression_type,
            TypedExpression::And {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Or {
                expression_type, ..
            } => *expression_type,
            TypedExpression::Cast {
                expression_type, ..
            } => *expression_type,
        }
    }

    pub fn to_polars(&self) -> polars::prelude::Expr {
        use polars::prelude::*;

        match self {
            TypedExpression::NullLiteral => lit(NULL),
            TypedExpression::BooleanLiteral { value } => lit(*value),
            TypedExpression::IntegerLiteral { value } => lit(*value),
            TypedExpression::FloatLiteral { value } => lit(*value),
            TypedExpression::StringLiteral { value } => lit(value.clone()),
            TypedExpression::Variable { name, .. } => col(name),
            TypedExpression::Positive { content, .. } => content.to_polars(),
            TypedExpression::Negative { content, .. } => -content.to_polars(),
            TypedExpression::Add { left, right, .. } => left.to_polars() + right.to_polars(),
            TypedExpression::Subtract { left, right, .. } => left.to_polars() - right.to_polars(),
            TypedExpression::Multiply { left, right, .. } => left.to_polars() * right.to_polars(),
            TypedExpression::TrueDivide { left, right, .. } => {
                binary_expr(left.to_polars(), Operator::TrueDivide, right.to_polars())
            }
            TypedExpression::FloorDivide { left, right, .. } => {
                left.to_polars().floor_div(right.to_polars())
            }
            TypedExpression::Mod { left, right, .. } => left.to_polars() % right.to_polars(),
            TypedExpression::Power { left, right, .. } => left.to_polars().pow(right.to_polars()),
            TypedExpression::Call { call } => call.to_polars(),
            TypedExpression::Equal { left, right, .. } => {
                left.to_polars().eq_missing(right.to_polars())
            }
            TypedExpression::NotEqual { left, right, .. } => {
                left.to_polars().neq_missing(right.to_polars())
            }
            TypedExpression::GreaterThanOrEqual { left, right, .. } => {
                left.to_polars().gt_eq(right.to_polars())
            }
            TypedExpression::LessThanOrEqual { left, right, .. } => {
                left.to_polars().lt_eq(right.to_polars())
            }
            TypedExpression::GreaterThan { left, right, .. } => {
                left.to_polars().gt(right.to_polars())
            }
            TypedExpression::LessThan { left, right, .. } => left.to_polars().lt(right.to_polars()),
            TypedExpression::Not { content, .. } => content.to_polars().not(),
            TypedExpression::And { left, right, .. } => left.to_polars().and(right.to_polars()),
            TypedExpression::Or { left, right, .. } => left.to_polars().or(right.to_polars()),
            TypedExpression::Cast {
                content,
                expression_type,
            } => content
                .to_polars()
                .cast(polars::datatypes::DataType::from(expression_type.data_type())),
        }
    }

    pub fn substitute(
        &self,
        substitutions: &std::collections::HashMap<&str, TypedExpression>,
    ) -> TypedExpression {
        match self {
            TypedExpression::NullLiteral => TypedExpression::NullLiteral,
            TypedExpression::BooleanLiteral { value } => {
                TypedExpression::BooleanLiteral { value: *value }
            }
            TypedExpression::IntegerLiteral { value } => {
                TypedExpression::IntegerLiteral { value: *value }
            }
            TypedExpression::FloatLiteral { value } => {
                TypedExpression::FloatLiteral { value: *value }
            }
            TypedExpression::StringLiteral { value } => TypedExpression::StringLiteral {
                value: value.clone(),
            },
            TypedExpression::Variable {
                name,
                expression_type,
            } => {
                if let Some(replacement) = substitutions.get(name.as_str()) {
                    replacement.clone()
                } else {
                    TypedExpression::Variable {
                        name: name.clone(),
                        expression_type: *expression_type,
                    }
                }
            }
            TypedExpression::Positive {
                content,
                expression_type,
            } => TypedExpression::Positive {
                content: Arc::new(content.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::Negative {
                content,
                expression_type,
            } => TypedExpression::Negative {
                content: Arc::new(content.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::Add {
                left,
                right,
                expression_type,
            } => TypedExpression::Add {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::Subtract {
                left,
                right,
                expression_type,
            } => TypedExpression::Subtract {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::Multiply {
                left,
                right,
                expression_type,
            } => TypedExpression::Multiply {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::TrueDivide {
                left,
                right,
                expression_type,
            } => TypedExpression::TrueDivide {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::FloorDivide {
                left,
                right,
                expression_type,
            } => TypedExpression::FloorDivide {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::Mod {
                left,
                right,
                expression_type,
            } => TypedExpression::Mod {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::Power {
                left,
                right,
                expression_type,
            } => TypedExpression::Power {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::Call { call } => TypedExpression::Call {
                call: call.substitute(substitutions),
            },
            TypedExpression::Equal {
                left,
                right,
                expression_type,
            } => TypedExpression::Equal {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::NotEqual {
                left,
                right,
                expression_type,
            } => TypedExpression::NotEqual {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::GreaterThanOrEqual {
                left,
                right,
                expression_type,
            } => TypedExpression::GreaterThanOrEqual {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::LessThanOrEqual {
                left,
                right,
                expression_type,
            } => TypedExpression::LessThanOrEqual {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::GreaterThan {
                left,
                right,
                expression_type,
            } => TypedExpression::GreaterThan {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::LessThan {
                left,
                right,
                expression_type,
            } => TypedExpression::LessThan {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::Not {
                content,
                expression_type,
            } => TypedExpression::Not {
                content: Arc::new(content.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::And {
                left,
                right,
                expression_type,
            } => TypedExpression::And {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::Or {
                left,
                right,
                expression_type,
            } => TypedExpression::Or {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
                expression_type: *expression_type,
            },
            TypedExpression::Cast {
                content,
                expression_type,
            } => TypedExpression::Cast {
                content: Arc::new(content.substitute(substitutions)),
                expression_type: *expression_type,
            },
        }
    }
}
