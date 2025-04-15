use pyo3::prelude::*;

#[pymodule]
pub mod functions {
    use ::std::sync::Arc;

    use crate::{expression::Expression, function, PyExpression};
    use pyo3::prelude::*;

    #[pyfunction]
    fn abs(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Abs {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn sqrt(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Sqrt {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn exp(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Exp {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn pow(base: &PyExpression, exponent: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Pow {
                    base: Arc::new(base.expression.clone()),
                    exponent: Arc::new(exponent.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn log(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Log {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn log2(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Log2 {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn log10(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Log10 {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn sin(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Sin {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn cos(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Cos {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn tan(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Tan {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn arcsin(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::ArcSin {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn arccos(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::ArcCos {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn arctan(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::ArcTan {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn floor(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Floor {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn ceil(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Ceil {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn to_boolean(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::ToBoolean {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn to_integer(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::ToInteger {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn to_float(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::ToFloat {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn to_string(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::ToString {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn max(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Max {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn min(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Min {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn same(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Same {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn n() -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::N {}),
            },
        }
    }

    #[pyfunction]
    fn row_index0() -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::RowIndex0 {}),
            },
        }
    }

    #[pyfunction]
    fn row_index1() -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::RowIndex1 {}),
            },
        }
    }

    #[pyfunction]
    fn is_null(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::IsNull {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn is_nan(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::IsNan {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn is_finite(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::IsFinite {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    #[pyo3(signature = (condition, then_branch, else_branch = None))]
    fn if_else(
        condition: &PyExpression,
        then_branch: &PyExpression,
        else_branch: Option<&PyExpression>,
    ) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::IfElse {
                    condition: Arc::new(condition.expression.clone()),
                    then_branch: Arc::new(then_branch.expression.clone()),
                    else_branch: Arc::new(
                        else_branch.map_or(Expression::NullLiteral, |e| e.expression.clone()),
                    ),
                }),
            },
        }
    }

    #[pyfunction]
    fn std(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Std {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn var(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Var {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn sum(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Sum {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn mean(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Mean {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn median(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Median {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn quantile(argument: &PyExpression, percentile: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Quantile {
                    argument: Arc::new(argument.expression.clone()),
                    quantile: Arc::new(percentile.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn trapz(t: &PyExpression, y: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Trapz {
                    t: Arc::new(t.expression.clone()),
                    y: Arc::new(y.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn interp(t: &PyExpression, ts: &PyExpression, ys: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Interp {
                    t: Arc::new(t.expression.clone()),
                    ts: Arc::new(ts.expression.clone()),
                    ys: Arc::new(ys.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn any(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Any {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn all(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::All {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn first(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::First {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }

    #[pyfunction]
    fn last(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                call: Arc::new(function::Last {
                    argument: Arc::new(argument.expression.clone()),
                }),
            },
        }
    }
}
