use crate::DataType;
use pyo3::{exceptions::PyTypeError, prelude::*};

#[pyclass(frozen, eq, extends=PyTypeError)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IncompatibleTypesError {
    #[pyo3(get)]
    pub operation: String,
    #[pyo3(get)]
    pub left_type: DataType,
    #[pyo3(get)]
    pub right_type: DataType,
}

impl<'py> IntoPyObject<'py> for IncompatibleTypesError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<IncompatibleTypesError>().call1((
            self.operation,
            self.left_type,
            self.right_type,
        ))
    }
}

#[pymethods]
impl IncompatibleTypesError {
    #[new]
    pub fn __new__(
        operation: String,
        left_type: DataType,
        right_type: DataType,
    ) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            operation,
            left_type,
            right_type,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Incompatible types for operation '{}': {} and {}",
            self.operation, self.left_type, self.right_type
        ))
    }
}
