use crate::expression::ast::Expression;
use std::collections::HashMap;
use std::sync::Arc;

impl Expression {
    pub fn substitute(&self, substitutions: &HashMap<&str, Expression>) -> Expression {
        match self {
            Expression::NullLiteral => self.clone(),
            Expression::BooleanLiteral { value: _ } => self.clone(),
            Expression::IntegerLiteral { value: _ } => self.clone(),
            Expression::FloatLiteral { value: _ } => self.clone(),
            Expression::StringLiteral { value: _ } => self.clone(),
            Expression::Variable { name } => {
                if let Some(substitution) = substitutions.get(name.as_str()) {
                    substitution.clone()
                } else {
                    self.clone()
                }
            }
            Expression::Positive { content } => Expression::Positive {
                content: Arc::new(content.substitute(substitutions)),
            },
            Expression::Negative { content } => Expression::Negative {
                content: Arc::new(content.substitute(substitutions)),
            },
            Expression::Add { left, right } => Expression::Add {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::Subtract { left, right } => Expression::Subtract {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::Multiply { left, right } => Expression::Multiply {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::TrueDivide { left, right } => Expression::TrueDivide {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::FloorDivide { left, right } => Expression::FloorDivide {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::Mod { left, right } => Expression::Mod {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::Power { left, right } => Expression::Power {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::Call { call } => Expression::Call {
                call: Arc::from(call.substitute(substitutions)),
            },
            Expression::Equal { left, right } => Expression::Equal {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::NotEqual { left, right } => Expression::NotEqual {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::GreaterThanOrEqual { left, right } => Expression::GreaterThanOrEqual {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::LessThanOrEqual { left, right } => Expression::LessThanOrEqual {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::GreaterThan { left, right } => Expression::GreaterThan {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::LessThan { left, right } => Expression::LessThan {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::Not { content } => Expression::Not {
                content: Arc::new(content.substitute(substitutions)),
            },
            Expression::And { left, right } => Expression::And {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
            Expression::Or { left, right } => Expression::Or {
                left: Arc::new(left.substitute(substitutions)),
                right: Arc::new(right.substitute(substitutions)),
            },
        }
    }
}
