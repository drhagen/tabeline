use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ColumnAlreadyExistsError {
    pub column_name: String,
}

impl<'py> IntoPyObject<'py> for ColumnAlreadyExistsError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<ColumnAlreadyExistsError>()
            .call1((self.column_name,))
    }
}

#[pymethods]
impl ColumnAlreadyExistsError {
    #[new]
    pub fn __new__(column_name: String) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { column_name })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Cannot create column {} as it already exists",
            self.column_name
        ))
    }
}
