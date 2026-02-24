use pyo3::{exceptions::PyTypeError, prelude::*};

#[pyclass(frozen, eq, extends=PyTypeError)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UnknownFunctionError {
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub available: Vec<String>,
}

impl<'py> IntoPyObject<'py> for UnknownFunctionError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<UnknownFunctionError>()
            .call1((self.name, self.available))
    }
}

#[pymethods]
impl UnknownFunctionError {
    #[new]
    pub fn __new__(name: String, available: Vec<String>) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { name, available })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Unknown function '{}'. Available functions: [{}]",
            self.name,
            self.available.join(", ")
        ))
    }
}
