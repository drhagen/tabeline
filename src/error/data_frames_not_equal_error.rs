use crate::testing::DataFrameDifference;

use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DataFramesNotEqualError {
    pub differences: Vec<DataFrameDifference>,
}

impl<'py> IntoPyObject<'py> for DataFramesNotEqualError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<DataFramesNotEqualError>()
            .call1((self.differences,))
    }
}

#[pymethods]
impl DataFramesNotEqualError {
    #[new]
    pub fn __new__(differences: Vec<DataFrameDifference>) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { differences })
    }

    pub fn __str__(&self) -> PyResult<String> {
        let mut output = String::from("DataFrames are not equal:");
        for diff in &self.differences {
            output.push_str(&format!("\n{}", diff));
        }
        Ok(output)
    }
}
