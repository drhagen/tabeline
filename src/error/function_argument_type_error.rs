use crate::DataType;
use pyo3::{exceptions::PyTypeError, prelude::*};

#[pyclass(frozen, eq, extends=PyTypeError)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FunctionArgumentTypeError {
    #[pyo3(get)]
    pub function: String,
    #[pyo3(get)]
    pub parameter: String,
    #[pyo3(get)]
    pub expected: String,
    #[pyo3(get)]
    pub actual: DataType,
}

impl<'py> IntoPyObject<'py> for FunctionArgumentTypeError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<FunctionArgumentTypeError>().call1((
            self.function,
            self.parameter,
            self.expected,
            self.actual,
        ))
    }
}

#[pymethods]
impl FunctionArgumentTypeError {
    #[new]
    pub fn __new__(
        function: String,
        parameter: String,
        expected: String,
        actual: DataType,
    ) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            function,
            parameter,
            expected,
            actual,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Function '{}' parameter '{}' expected {}, got {}",
            self.function, self.parameter, self.expected, self.actual
        ))
    }
}
