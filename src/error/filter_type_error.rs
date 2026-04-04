use crate::DataType;
use pyo3::{exceptions::PyTypeError, prelude::*};

#[pyclass(frozen, eq, extends=PyTypeError, from_py_object)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FilterTypeError {
    #[pyo3(get)]
    pub actual_type: DataType,
}

impl<'py> IntoPyObject<'py> for FilterTypeError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<FilterTypeError>().call1((self.actual_type,))
    }
}

#[pymethods]
impl FilterTypeError {
    #[new]
    pub fn __new__(actual_type: DataType) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { actual_type })
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Filter requires Boolean predicate, got {}",
            self.actual_type
        ))
    }
}
