use pyo3::{exceptions::PyException, prelude::*};

use crate::testing::ArrayDifference;

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ArraysNotEqualError {
    pub differences: Vec<ArrayDifference>,
}

impl<'py> IntoPyObject<'py> for ArraysNotEqualError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<ArraysNotEqualError>()
            .call1((self.differences,))
    }
}

#[pymethods]
impl ArraysNotEqualError {
    #[new]
    pub fn __new__(differences: Vec<ArrayDifference>) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self { differences })
    }

    pub fn __str__(&self) -> PyResult<String> {
        let mut output = String::from("Arrays are not equal:");
        for diff in &self.differences {
            output.push_str(&format!("\n{}", diff));
        }
        Ok(output)
    }
}
