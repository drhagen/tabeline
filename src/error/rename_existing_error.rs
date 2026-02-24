use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RenameExistingError {
    #[pyo3(get)]
    pub old_column: String,
    #[pyo3(get)]
    pub new_column: String,
}

impl<'py> IntoPyObject<'py> for RenameExistingError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<RenameExistingError>()
            .call1((self.old_column, self.new_column))
    }
}

#[pymethods]
impl RenameExistingError {
    #[new]
    pub fn __new__(old_column: String, new_column: String) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            old_column,
            new_column,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Cannot rename {} to {} because {} already exists",
            self.old_column, self.new_column, self.new_column
        ))
    }
}
