use polars::prelude::*;
use pyo3::{
    exceptions::{PyIndexError, PyStopIteration},
    prelude::*,
    types::PyList,
    IntoPyObjectExt,
};

use crate::{
    arrow::{polars_arrow_array_from_pyarrow, pyarrow_array_from_polars_arrow_array},
    error::IncompatibleTypeError,
    py_scalar::PyScalar,
    DataType, IndexOutOfBoundsError,
};

#[pyclass(frozen, eq, sequence)]
#[derive(Debug, Clone, PartialEq)]
pub struct PyArray {
    pub(crate) polars_column: Column,
}

fn collect_elements_of_given_type<T>(
    elements: &Bound<'_, PyList>,
    data_type: DataType,
) -> PyResult<Column>
where
    for<'py> T: FromPyObject<'py>,
    Series: FromIterator<Option<T>>,
{
    let converted_elements = elements
        .iter()
        .enumerate()
        .map(|(i, item)| {
            if item.is_none() {
                Ok(None)
            } else {
                match item.extract::<T>() {
                    Ok(value) => Ok(Some(value)),
                    Err(_) => Err(PyErr::from_value(
                        IncompatibleTypeError {
                            expected_type: data_type,
                            item: item.into(),
                            location: i,
                        }
                        .into_bound_py_any(elements.py())?,
                    )),
                }
            }
        })
        .collect::<Result<Vec<Option<T>>, PyErr>>()?;

    Ok(Series::from_iter(converted_elements).into_column())
}

#[pyclass]
struct PyArrayIterator {
    polars_column: Column,
    position: usize,
}

#[pymethods]
impl PyArrayIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<'_, Self>, py: Python<'_>) -> PyResult<PyScalar> {
        match slf.polars_column.get(slf.position) {
            Ok(value) => {
                // value holds onto the lifetime of the column, so we need to
                // bind it before we can mutate
                let py_value = PyScalar::from(value);
                slf.position += 1;
                Ok(py_value)
            }
            Err(_) => Err(PyStopIteration::new_err(py.None())),
        }
    }
}

#[pymethods]
impl PyArray {
    #[staticmethod]
    #[pyo3(signature = (elements, /, data_type))]
    pub fn from_list(elements: &Bound<'_, PyList>, data_type: DataType) -> PyResult<PyArray> {
        // Use the data type to convert each element to that type. Raise an exception if the
        // element is not compatible with the data type.
        let polars_data_type = data_type.into();

        let series = match data_type {
            DataType::Boolean => collect_elements_of_given_type::<bool>(elements, data_type)?,
            DataType::Integer8 => collect_elements_of_given_type::<i8>(elements, data_type)?,
            DataType::Integer16 => collect_elements_of_given_type::<i16>(elements, data_type)?,
            DataType::Integer32 => collect_elements_of_given_type::<i32>(elements, data_type)?,
            DataType::Integer64 => collect_elements_of_given_type::<i64>(elements, data_type)?,
            DataType::Whole8 => collect_elements_of_given_type::<u8>(elements, data_type)?,
            DataType::Whole16 => collect_elements_of_given_type::<u16>(elements, data_type)?,
            DataType::Whole32 => collect_elements_of_given_type::<u32>(elements, data_type)?,
            DataType::Whole64 => collect_elements_of_given_type::<u64>(elements, data_type)?,
            DataType::Float32 => collect_elements_of_given_type::<f32>(elements, data_type)?,
            DataType::Float64 => collect_elements_of_given_type::<f64>(elements, data_type)?,
            DataType::String => collect_elements_of_given_type::<String>(elements, data_type)?,
            DataType::Nothing => {
                // Apparently, `collect_elements_of_given_type::<!>` is not supported,
                // so duplicate the checking code, but use new_scalar to actually create.
                for (i, item) in elements.iter().enumerate() {
                    if !item.is_none() {
                        return Err(PyErr::from_value(
                            IncompatibleTypeError {
                                expected_type: data_type,
                                item: item.into(),
                                location: i,
                            }
                            .into_bound_py_any(elements.py())?,
                        ));
                    }
                }

                Column::new_scalar(
                    "".into(),
                    Scalar::new(polars_data_type, AnyValue::Null),
                    elements.len(),
                )
            }
        };

        Ok(PyArray {
            polars_column: series,
        })
    }

    #[getter]
    pub fn data_type(&self) -> DataType {
        self.polars_column.dtype().into()
    }

    fn __len__(&self) -> usize {
        self.len()
    }

    fn __iter__(&self) -> PyArrayIterator {
        PyArrayIterator {
            polars_column: self.polars_column.clone(),
            position: 0,
        }
    }

    fn item(&self, key: usize) -> PyResult<PyScalar> {
        let value = self.polars_column.get(key);
        match value {
            Ok(value) => Ok(PyScalar::from(value)),
            Err(_) => Err(PyIndexError::new_err("Array index out of range")),
        }
    }

    #[pyo3(signature = (start, stop, step))]
    fn slice_range0(&self, start: usize, stop: usize, step: usize) -> PyArray {
        let out_column = self
            .polars_column
            .slice(start as i64, stop - start)
            .gather_every(step, 0)
            .unwrap();
        PyArray {
            polars_column: out_column,
        }
    }

    #[pyo3(signature = (indexes, /))]
    fn slice0(&self, indexes: Vec<IdxSize>, py: Python) -> PyResult<PyArray> {
        for &index in &indexes {
            if index >= self.polars_column.len() as u32 {
                return Err(PyErr::from_value(
                    IndexOutOfBoundsError {
                        index: index as i64,
                        length: self.polars_column.len() as i64,
                        one_indexed: false,
                    }
                    .into_bound_py_any(py)?,
                ));
            }
        }

        let polars_column = self.polars_column.take_slice(indexes.as_slice()).unwrap();

        Ok(PyArray { polars_column })
    }

    #[staticmethod]
    #[pyo3(signature = (pyarrow_array, /))]
    fn from_pyarrow_array(pyarrow_array: &Bound<'_, PyAny>) -> PyResult<PyArray> {
        // Import the array
        let polars_arrow_array = polars_arrow_array_from_pyarrow(pyarrow_array)?;

        // Use polars' functionality to convert from PyArrow to Polars Series
        let series =
            Series::try_from((Into::<PlSmallStr>::into(""), polars_arrow_array.clone())).unwrap();

        // Convert Series to Column
        let polars_column = series.into_column();

        // Return a new PyArray with the column
        Ok(PyArray { polars_column })
    }

    #[pyo3(signature = ())]
    fn to_pyarrow_array(&self) -> PyResult<Py<PyAny>> {
        // Convert Column to contiguous Series
        let series = self
            .polars_column
            // .clone()
            .as_materialized_series()
            .rechunk();

        // Convert Series to Arrow
        let array = series.to_arrow(0, CompatLevel::oldest());
        let field = series.field().to_arrow(CompatLevel::oldest());

        Python::attach(|py| {
            let pyarrow = py.import("pyarrow")?;

            let pyarrow_array = pyarrow_array_from_polars_arrow_array(&pyarrow, array, &field)?;

            // Return the PyArrow array
            Ok(pyarrow_array.unbind())
        })
    }
}

impl PyArray {
    pub fn is_empty(&self) -> bool {
        self.polars_column.is_empty()
    }

    pub fn len(&self) -> usize {
        self.polars_column.len()
    }
}
