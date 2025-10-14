use crate::function::Function;
use polars::prelude::*;
use std::{fmt::Debug, sync::Arc};

#[derive(Debug, Clone, PartialEq)]
pub enum Expression {
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
    },
    Positive {
        content: Arc<Expression>,
    },
    Negative {
        content: Arc<Expression>,
    },
    Add {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    Subtract {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    Multiply {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    TrueDivide {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    FloorDivide {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    Mod {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    Power {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    Call {
        call: Arc<dyn Function>,
    },
    Equal {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    NotEqual {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    GreaterThanOrEqual {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    LessThanOrEqual {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    GreaterThan {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    LessThan {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    Not {
        content: Arc<Expression>,
    },
    And {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
    Or {
        left: Arc<Expression>,
        right: Arc<Expression>,
    },
}

impl Expression {
    pub fn to_polars(&self) -> Expr {
        match self {
            Expression::NullLiteral => lit(NULL),
            Expression::BooleanLiteral { value } => lit(*value),
            Expression::IntegerLiteral { value } => lit(*value),
            Expression::FloatLiteral { value } => lit(*value),
            Expression::StringLiteral { value } => lit(value.clone()),
            Expression::Variable { name } => col(name),
            Expression::Positive { content } => content.to_polars(),
            Expression::Negative { content } => -content.to_polars(),
            Expression::Add { left, right } => left.to_polars() + right.to_polars(),
            Expression::Subtract { left, right } => left.to_polars() - right.to_polars(),
            Expression::Multiply { left, right } => left.to_polars() * right.to_polars(),
            Expression::TrueDivide { left, right } => {
                // There is not true divide operator or method on Expr
                binary_expr(left.to_polars(), Operator::TrueDivide, right.to_polars())
            }
            Expression::FloorDivide { left, right } => {
                left.to_polars().floor_div(right.to_polars())
            }
            Expression::Mod { left, right } => left.to_polars() % right.to_polars(),
            Expression::Power { left, right } => left.to_polars().pow(right.to_polars()),
            Expression::Call { call } => call.to_polars(),
            Expression::Equal { left, right } => left.to_polars().eq_missing(right.to_polars()),
            Expression::NotEqual { left, right } => left.to_polars().neq_missing(right.to_polars()),
            Expression::GreaterThanOrEqual { left, right } => {
                left.to_polars().gt_eq(right.to_polars())
            }
            Expression::LessThanOrEqual { left, right } => {
                left.to_polars().lt_eq(right.to_polars())
            }
            Expression::GreaterThan { left, right } => left.to_polars().gt(right.to_polars()),
            Expression::LessThan { left, right } => left.to_polars().lt(right.to_polars()),
            Expression::Not { content } => content.to_polars().not(),
            Expression::And { left, right } => left.to_polars().and(right.to_polars()),
            Expression::Or { left, right } => left.to_polars().or(right.to_polars()),
        }
    }
}
