use pyo3::{exceptions::PyIndexError, prelude::*};

#[pyclass(frozen, eq, extends=PyIndexError)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IndexOutOfBoundsError {
    pub index: i64,
    pub length: i64,
    pub one_indexed: bool,
}

impl<'py> IntoPyObject<'py> for IndexOutOfBoundsError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<IndexOutOfBoundsError>()
            .call1((self.index, self.length, self.one_indexed))
    }
}

#[pymethods]
impl IndexOutOfBoundsError {
    #[new]
    pub fn __new__(index: i64, length: i64, one_indexed: bool) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            index,
            length,
            one_indexed,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        let base_string = if self.one_indexed { "one" } else { "zero" };
        let first_index = if self.one_indexed { 1 } else { 0 };
        Ok(format!(
            "Cannot get index {} ({}-based) less than the first index ({}) or greater than length ({})",
            self.index, base_string, first_index, self.length
        ))
    }
}
