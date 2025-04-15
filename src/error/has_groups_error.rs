use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HasGroupsError {
    pub group_levels: Vec<Vec<String>>,
}

impl<'py> IntoPyObject<'py> for HasGroupsError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<HasGroupsError>().call1((self.group_levels,))
    }
}

#[pymethods]
impl HasGroupsError {
    #[new]
    pub fn __new__(group_levels: Vec<Vec<String>>) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { group_levels })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Cannot perform this operation when groups are present, found {:?}",
            self.group_levels
        ))
    }
}
