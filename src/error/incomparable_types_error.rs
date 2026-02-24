use crate::DataType;
use pyo3::{exceptions::PyTypeError, prelude::*};

#[pyclass(frozen, eq, extends=PyTypeError)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IncomparableTypesError {
    #[pyo3(get)]
    pub left_type: DataType,
    #[pyo3(get)]
    pub right_type: DataType,
}

impl<'py> IntoPyObject<'py> for IncomparableTypesError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<IncomparableTypesError>()
            .call1((self.left_type, self.right_type))
    }
}

#[pymethods]
impl IncomparableTypesError {
    #[new]
    pub fn __new__(left_type: DataType, right_type: DataType) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            left_type,
            right_type,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Cannot compare types {} and {}",
            self.left_type, self.right_type
        ))
    }
}
