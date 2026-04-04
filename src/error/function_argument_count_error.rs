use pyo3::{exceptions::PyTypeError, prelude::*};

#[pyclass(frozen, eq, extends=PyTypeError, from_py_object)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FunctionArgumentCountError {
    #[pyo3(get)]
    pub function: String,
    #[pyo3(get)]
    pub expected: usize,
    #[pyo3(get)]
    pub actual: usize,
}

impl<'py> IntoPyObject<'py> for FunctionArgumentCountError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<FunctionArgumentCountError>().call1((
            self.function,
            self.expected,
            self.actual,
        ))
    }
}

#[pymethods]
impl FunctionArgumentCountError {
    #[new]
    pub fn __new__(function: String, expected: usize, actual: usize) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            function,
            expected,
            actual,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Function '{}' expects {} arguments, got {}",
            self.function, self.expected, self.actual
        ))
    }
}
