use pyo3::prelude::*;

#[pymodule]
pub mod functions {
    use ::std::sync::Arc;

    use crate::{expression::Expression, PyExpression};
    use pyo3::prelude::*;

    #[pyfunction]
    fn abs(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "abs".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn sqrt(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "sqrt".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn exp(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "exp".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn pow(base: &PyExpression, exponent: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "pow".to_string(),
                arguments: vec![
                    Arc::new(base.expression.clone()),
                    Arc::new(exponent.expression.clone()),
                ],
            },
        }
    }

    #[pyfunction]
    fn log(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "log".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn log2(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "log2".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn log10(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "log10".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn sin(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "sin".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn cos(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "cos".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn tan(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "tan".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn arcsin(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "arcsin".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn arccos(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "arccos".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn arctan(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "arctan".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn floor(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "floor".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn ceil(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "ceil".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn to_boolean(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "to_boolean".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn to_integer(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "to_integer".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn to_float(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "to_float".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn to_string(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "to_string".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn max(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "max".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn min(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "min".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn same(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "same".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn n() -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "n".to_string(),
                arguments: vec![],
            },
        }
    }

    #[pyfunction]
    fn row_index0() -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "row_index0".to_string(),
                arguments: vec![],
            },
        }
    }

    #[pyfunction]
    fn row_index1() -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "row_index1".to_string(),
                arguments: vec![],
            },
        }
    }

    #[pyfunction]
    fn is_null(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "is_null".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn is_nan(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "is_nan".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn is_finite(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "is_finite".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    #[pyo3(signature = (arg, *args))]
    fn pmax(arg: &PyExpression, args: Vec<pyo3::PyRef<PyExpression>>) -> PyExpression {
        let mut arguments: Vec<Arc<Expression>> = vec![Arc::new(arg.expression.clone())];
        arguments.extend(args.iter().map(|a| Arc::new(a.expression.clone())));

        PyExpression {
            expression: Expression::Call {
                name: "pmax".to_string(),
                arguments,
            },
        }
    }

    #[pyfunction]
    #[pyo3(signature = (arg, *args))]
    fn pmin(arg: &PyExpression, args: Vec<pyo3::PyRef<PyExpression>>) -> PyExpression {
        let mut arguments: Vec<Arc<Expression>> = vec![Arc::new(arg.expression.clone())];
        arguments.extend(args.iter().map(|a| Arc::new(a.expression.clone())));

        PyExpression {
            expression: Expression::Call {
                name: "pmin".to_string(),
                arguments,
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
                name: "if_else".to_string(),
                arguments: vec![
                    Arc::new(condition.expression.clone()),
                    Arc::new(then_branch.expression.clone()),
                    Arc::new(else_branch.map_or(Expression::NullLiteral, |e| e.expression.clone())),
                ],
            },
        }
    }

    #[pyfunction]
    fn std(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "std".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn var(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "var".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn sum(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "sum".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn mean(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "mean".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn median(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "median".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn quantile(argument: &PyExpression, percentile: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "quantile".to_string(),
                arguments: vec![
                    Arc::new(argument.expression.clone()),
                    Arc::new(percentile.expression.clone()),
                ],
            },
        }
    }

    #[pyfunction]
    fn trapz(t: &PyExpression, y: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "trapz".to_string(),
                arguments: vec![
                    Arc::new(t.expression.clone()),
                    Arc::new(y.expression.clone()),
                ],
            },
        }
    }

    #[pyfunction]
    fn interp(t: &PyExpression, ts: &PyExpression, ys: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "interp".to_string(),
                arguments: vec![
                    Arc::new(t.expression.clone()),
                    Arc::new(ts.expression.clone()),
                    Arc::new(ys.expression.clone()),
                ],
            },
        }
    }

    #[pyfunction]
    fn any(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "any".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn all(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "all".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn first(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "first".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }

    #[pyfunction]
    fn last(argument: &PyExpression) -> PyExpression {
        PyExpression {
            expression: Expression::Call {
                name: "last".to_string(),
                arguments: vec![Arc::new(argument.expression.clone())],
            },
        }
    }
}
