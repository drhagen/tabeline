use polars::prelude::AnyValue;
use pyo3::{exceptions::PyTypeError, prelude::*, types::PyNone, IntoPyObjectExt};
use std::fmt::Display;

/**
 * A wrapper for Python primitive types.
 *
 * This allows sending and recieving Python primitives via PyO3.
 *
 * # Variants
 *
 * - `Int` - Maps a Rust i64 to a Python int
 * - `Float` - Maps a Rust f64 to a Python float
 * - `Bool` - Maps a Rust bool to a Python bool
 * - `String` - Maps a Rust String to a Python str
 * - `Null` - Maps to Python None
 */
#[derive(Debug, Clone)]
pub enum PyScalar {
    Bool(bool),
    Int(i64),
    Float(f64),
    String(String),
    Null,
}

impl Eq for PyScalar {}

impl PartialEq for PyScalar {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (Self::Bool(a), Self::Bool(b)) => a == b,
            (Self::Int(a), Self::Int(b)) => a == b,
            (Self::Float(a), Self::Float(b)) => {
                // nan == nan
                // -0.0 != 0.0
                if a.is_nan() && b.is_nan() {
                    true
                } else {
                    a == b && a.is_sign_positive() == b.is_sign_positive()
                }
            }
            (Self::String(a), Self::String(b)) => a == b,
            (Self::Null, Self::Null) => true,
            _ => false,
        }
    }
}

impl Display for PyScalar {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            PyScalar::Bool(x) => write!(f, "{}", x),
            PyScalar::Int(x) => write!(f, "{}", x),
            PyScalar::Float(x) => write!(f, "{}", x),
            PyScalar::String(x) => write!(f, "{}", x),
            PyScalar::Null => write!(f, "null"),
        }
    }
}

impl<'py> FromPyObject<'py> for PyScalar {
    fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        if let Ok(val) = ob.extract::<bool>() {
            return Ok(PyScalar::Bool(val));
        }
        if let Ok(val) = ob.extract::<i64>() {
            return Ok(PyScalar::Int(val));
        }
        if let Ok(val) = ob.extract::<f64>() {
            return Ok(PyScalar::Float(val));
        }
        if let Ok(val) = ob.extract::<String>() {
            return Ok(PyScalar::String(val));
        }
        if ob.is_none() {
            return Ok(PyScalar::Null);
        }
        Err(PyTypeError::new_err(
            "Expected a scalar value (int, float, bool, str, or None)",
        ))
    }
}

impl<'py> IntoPyObject<'py> for PyScalar {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            PyScalar::Bool(val) => val.into_bound_py_any(py),
            PyScalar::Int(val) => val.into_bound_py_any(py),
            PyScalar::Float(val) => val.into_bound_py_any(py),
            PyScalar::String(val) => val.into_bound_py_any(py),
            PyScalar::Null => PyNone::get(py).into_bound_py_any(py),
        }
    }
}

impl From<AnyValue<'_>> for PyScalar {
    fn from(value: AnyValue) -> Self {
        match value {
            AnyValue::Null => PyScalar::Null,
            AnyValue::Boolean(value) => PyScalar::Bool(value),
            AnyValue::UInt8(value) => PyScalar::Int(value as i64),
            AnyValue::UInt16(value) => PyScalar::Int(value as i64),
            AnyValue::UInt32(value) => PyScalar::Int(value as i64),
            AnyValue::UInt64(value) => PyScalar::Int(value as i64),
            AnyValue::Int8(value) => PyScalar::Int(value as i64),
            AnyValue::Int16(value) => PyScalar::Int(value as i64),
            AnyValue::Int32(value) => PyScalar::Int(value as i64),
            AnyValue::Int64(value) => PyScalar::Int(value),
            AnyValue::Float32(value) => PyScalar::Float(value as f64),
            AnyValue::Float64(value) => PyScalar::Float(value),
            AnyValue::String(value) => PyScalar::String(value.to_owned()),
            // WORKAROUND: Series.from_iter generates owned strings when given a list of length 1
            AnyValue::StringOwned(value) => PyScalar::String(value.into()),
            any_value => panic!("Unsupported data type: {:?}", any_value.dtype()),
        }
    }
}
