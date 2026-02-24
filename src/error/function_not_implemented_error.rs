use pyo3::{exceptions::PyNotImplementedError, prelude::*};

#[pyclass(frozen, eq, extends=PyNotImplementedError)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FunctionNotImplementedError {
    #[pyo3(get)]
    pub function: String,
}

impl<'py> IntoPyObject<'py> for FunctionNotImplementedError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<FunctionNotImplementedError>()
            .call1((self.function,))
    }
}

#[pymethods]
impl FunctionNotImplementedError {
    #[new]
    pub fn __new__(function: String) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { function })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Function '{}' validation not yet implemented",
            self.function
        ))
    }
}
