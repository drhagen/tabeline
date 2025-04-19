use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NonexistentColumnError {
    pub column_name: String,
    pub existing_column_names: Vec<String>,
}

impl<'py> IntoPyObject<'py> for NonexistentColumnError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<NonexistentColumnError>()
            .call1((self.column_name, self.existing_column_names))
    }
}

#[pymethods]
impl NonexistentColumnError {
    #[new]
    pub fn __new__(
        column_name: String,
        existing_column_names: Vec<String>,
    ) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            column_name,
            existing_column_names,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        let existing_column_names_string = self.existing_column_names.join(", ");
        Ok(format!(
            "Expected to find column {}, but it was not among existing columns {}",
            self.column_name, existing_column_names_string
        ))
    }
}
