use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GroupColumnError {
    pub column_name: String,
}

impl<'py> IntoPyObject<'py> for GroupColumnError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<GroupColumnError>().call1((self.column_name,))
    }
}

#[pymethods]
impl GroupColumnError {
    #[new]
    pub fn __new__(column_name: String) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { column_name })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Cannot perform this operation on group column {}",
            self.column_name
        ))
    }
}
