use pyo3::{exceptions::PyTypeError, prelude::*};

#[pyclass(frozen, eq, extends=PyTypeError, from_py_object)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SummarizeTypeError {
    #[pyo3(get)]
    pub column: String,
}

impl<'py> IntoPyObject<'py> for SummarizeTypeError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<SummarizeTypeError>().call1((self.column,))
    }
}

#[pymethods]
impl SummarizeTypeError {
    #[new]
    pub fn __new__(column: String) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { column })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Summarize requires scalar expression for column '{}', got array expression",
            self.column
        ))
    }
}
