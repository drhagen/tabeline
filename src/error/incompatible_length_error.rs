use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IncompatibleLengthError {
    pub expected_length: usize,
    pub actual_length: usize,
    pub column_name: String,
}

impl<'py> IntoPyObject<'py> for IncompatibleLengthError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<IncompatibleLengthError>().call1((
            self.expected_length,
            self.actual_length,
            self.column_name,
        ))
    }
}

#[pymethods]
impl IncompatibleLengthError {
    #[new]
    pub fn __new__(
        expected_length: usize,
        actual_length: usize,
        column_name: String,
    ) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            expected_length,
            actual_length,
            column_name,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Expected all columns to have length {}, but got length {} in column {}",
            self.expected_length, self.actual_length, self.column_name
        ))
    }
}
