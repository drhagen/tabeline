use pyo3::{exceptions::PyException, prelude::*};

#[pyclass(frozen, eq, extends=PyException)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UnmatchedGroupLevelsError {
    pub expected_group_levels: Vec<Vec<String>>,
    pub actual_group_levels: Vec<Vec<String>>,
}

impl<'py> IntoPyObject<'py> for UnmatchedGroupLevelsError {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        py.get_type::<UnmatchedGroupLevelsError>()
            .call1((self.expected_group_levels, self.actual_group_levels))
    }
}

#[pymethods]
impl UnmatchedGroupLevelsError {
    #[new]
    pub fn __new__(
        expected_group_levels: Vec<Vec<String>>,
        actual_group_levels: Vec<Vec<String>>,
    ) -> PyClassInitializer<Self> {
        PyClassInitializer::from(Self {
            expected_group_levels,
            actual_group_levels,
        })
    }

    pub fn __str__(&self) -> PyResult<String> {
        let expected_str = self
            .expected_group_levels
            .iter()
            .map(|level| format!("[{}]", level.join(",")))
            .collect::<Vec<_>>()
            .join(",");

        let actual_str = self
            .actual_group_levels
            .iter()
            .map(|level| format!("[{}]", level.join(",")))
            .collect::<Vec<_>>()
            .join(",");

        Ok(format!(
            "Group levels do not match; expected {} but got {}",
            expected_str, actual_str
        ))
    }
}
