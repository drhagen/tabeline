use pyo3::{exceptions::PyIndexError, prelude::*};

// WORKAROUND: Polars does not return a useful payload when indexing fails, so
// this only contains the not-particularly-helpful message from Polars.
#[pyclass(frozen, eq, extends=PyIndexError)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GroupIndexOutOfBoundsError {
    pub message: String,
}

impl<'py> IntoPyObject<'py> for GroupIndexOutOfBoundsError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<GroupIndexOutOfBoundsError>()
            .call1((self.message,))
    }
}

#[pymethods]
impl GroupIndexOutOfBoundsError {
    #[new]
    pub fn __new__(message: String) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { message })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(self.message.clone())
    }
}
