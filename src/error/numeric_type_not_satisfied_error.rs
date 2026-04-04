use crate::DataType;
use pyo3::{exceptions::PyTypeError, prelude::*};

#[pyclass(frozen, eq, extends=PyTypeError, from_py_object)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NumericTypeNotSatisfiedError {
    #[pyo3(get)]
    pub operation: String,
    #[pyo3(get)]
    pub actual: DataType,
}

impl<'py> IntoPyObject<'py> for NumericTypeNotSatisfiedError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<NumericTypeNotSatisfiedError>()
            .call1((self.operation, self.actual))
    }
}

#[pymethods]
impl NumericTypeNotSatisfiedError {
    #[new]
    pub fn __new__(operation: String, actual: DataType) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { operation, actual })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Expected numeric type in operation `{}`, but found {}",
            self.operation, self.actual
        ))
    }
}
