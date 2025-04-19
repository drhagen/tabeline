use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UnmatchedColumnsError {
    pub expected_columns: Vec<String>,
    pub actual_columns: Vec<String>,
}

impl<'py> IntoPyObject<'py> for UnmatchedColumnsError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<UnmatchedColumnsError>()
            .call1((self.expected_columns, self.actual_columns))
    }
}

#[pymethods]
impl UnmatchedColumnsError {
    #[new]
    pub fn __new__(
        expected_columns: Vec<String>,
        actual_columns: Vec<String>,
    ) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            expected_columns,
            actual_columns,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Columns do not match\nExpected columns: {:?}\nActual columns: {:?}",
            self.expected_columns, self.actual_columns
        ))
    }
}
