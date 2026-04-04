use crate::DataType;
use pyo3::{exceptions::PyTypeError, prelude::*};

#[pyclass(frozen, eq, extends=PyTypeError, from_py_object)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TypeMismatchError {
    #[pyo3(get)]
    pub operation: String,
    #[pyo3(get)]
    pub expected: DataType,
    #[pyo3(get)]
    pub actual: DataType,
}

impl<'py> IntoPyObject<'py> for TypeMismatchError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<TypeMismatchError>()
            .call1((self.operation, self.expected, self.actual))
    }
}

#[pymethods]
impl TypeMismatchError {
    #[new]
    pub fn __new__(
        operation: String,
        expected: DataType,
        actual: DataType,
    ) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            operation,
            expected,
            actual,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Expected {} in operation `{}`, but found {}",
            self.expected, self.operation, self.actual
        ))
    }
}
