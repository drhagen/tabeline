use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NoGroupsError {}

impl<'py> IntoPyObject<'py> for NoGroupsError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<NoGroupsError>().call1(())
    }
}

#[pymethods]
impl NoGroupsError {
    #[new]
    pub fn __new__() -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {})
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok("Cannot perform this operation on a data frame with no group levels".to_string())
    }
}
