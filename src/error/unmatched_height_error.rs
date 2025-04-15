use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UnmatchedHeightError {
    pub expected_height: usize,
    pub actual_height: usize,
}

impl<'py> IntoPyObject<'py> for UnmatchedHeightError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<UnmatchedHeightError>()
            .call1((self.expected_height, self.actual_height))
    }
}

#[pymethods]
impl UnmatchedHeightError {
    #[new]
    pub fn __new__(expected_height: usize, actual_height: usize) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            expected_height,
            actual_height,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Heights do not match; expected {} but got {}",
            self.expected_height, self.actual_height
        ))
    }
}
