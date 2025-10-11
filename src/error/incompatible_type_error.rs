use crate::DataType;
use pyo3::types::PyAnyMethods;
use pyo3::{exceptions::PyTypeError, prelude::*};

#[pyclass(frozen, extends=PyTypeError)]
#[derive(Debug)]
pub struct IncompatibleTypeError {
    pub expected_type: DataType,
    pub item: Py<PyAny>,
    pub location: usize,
}

impl<'py> IntoPyObject<'py> for IncompatibleTypeError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<IncompatibleTypeError>()
            .call1((self.expected_type, self.item, self.location))
    }
}

#[pymethods]
impl IncompatibleTypeError {
    #[new]
    pub fn __new__(
        expected_type: DataType,
        item: Py<PyAny>,
        location: usize,
    ) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            expected_type,
            item,
            location,
        })
    }

    fn __eq__(&self, other: &Self, py: Python) -> PyResult<bool> {
        Ok(self.expected_type == other.expected_type
            && self.item.bind(py).eq(other.item.bind(py))?
            && self.location == other.location)
    }

    fn __str__(&self, py: Python) -> PyResult<String> {
        let item_type = self.item.bind(py).get_type().name().unwrap();

        Ok(format!(
            "Expected elements convertable to data type {} or None, but the element {} at index {} has type {}",
            self.expected_type, self.item, self.location, item_type
        ))
    }
}
