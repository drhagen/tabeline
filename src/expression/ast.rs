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
        name: String,
        arguments: Vec<Arc<Expression>>,
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
