use std::sync::Arc;

use pyo3::prelude::*;

use crate::expression::Expression;

#[pyclass(frozen)]
#[derive(Debug, Clone, PartialEq)]
pub struct PyExpression {
    pub expression: Expression,
}

#[pymethods]
impl PyExpression {
    #[staticmethod]
    fn null() -> Self {
        Self {
            expression: Expression::NullLiteral,
        }
    }

    #[staticmethod]
    fn boolean(value: bool) -> Self {
        Self {
            expression: Expression::BooleanLiteral { value },
        }
    }

    #[staticmethod]
    fn integer(value: i64) -> Self {
        Self {
            expression: Expression::IntegerLiteral { value },
        }
    }

    #[staticmethod]
    fn float(value: f64) -> Self {
        Self {
            expression: Expression::FloatLiteral { value },
        }
    }

    #[staticmethod]
    fn string(value: String) -> Self {
        Self {
            expression: Expression::StringLiteral { value },
        }
    }

    #[staticmethod]
    fn variable(name: String) -> Self {
        Self {
            expression: Expression::Variable { name },
        }
    }

    fn positive(&self) -> Self {
        Self {
            expression: Expression::Positive {
                content: Arc::new(self.expression.clone()),
            },
        }
    }

    fn negative(&self) -> Self {
        Self {
            expression: Expression::Negative {
                content: Arc::new(self.expression.clone()),
            },
        }
    }
    fn add(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::Add {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }
    fn subtract(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::Subtract {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn multiply(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::Multiply {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn true_divide(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::TrueDivide {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn floor_divide(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::FloorDivide {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn modulo(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::Mod {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn power(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::Power {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    // fn call(&self, function: PyFunction) -> Self {
    //     Self {
    //         expression: Expression::Call {
    //             function: Arc::new(function),
    //         },
    //     }
    // }

    fn equal(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::Equal {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn not_equal(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::NotEqual {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn greater_than_or_equal(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::GreaterThanOrEqual {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn less_than_or_equal(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::LessThanOrEqual {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn greater_than(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::GreaterThan {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn less_than(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::LessThan {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn not_(&self) -> Self {
        Self {
            expression: Expression::Not {
                content: Arc::new(self.expression.clone()),
            },
        }
    }

    fn and_(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::And {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }

    fn or_(&self, other: &PyExpression) -> Self {
        Self {
            expression: Expression::Or {
                left: Arc::new(self.expression.clone()),
                right: Arc::new(other.expression.clone()),
            },
        }
    }
}
