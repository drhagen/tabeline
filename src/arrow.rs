use polars::prelude::*;
use polars_arrow::{array::Array, datatypes::Field, ffi, record_batch::RecordBatchT};
use pyo3::{ffi::Py_uintptr_t, prelude::*};

pub fn polars_arrow_array_from_pyarrow(pyarrow_array: &Bound<PyAny>) -> PyResult<Box<dyn Array>> {
    // record_batch must be a pyarrow.RecordBatch
    let mut array_box = Box::new(ffi::ArrowArray::empty());
    let mut schema_box = Box::new(ffi::ArrowSchema::empty());

    // Get pointers to the boxes
    let array_ptr = array_box.as_mut() as *mut ffi::ArrowArray;
    let schema_ptr = schema_box.as_mut() as *mut ffi::ArrowSchema;

    // Export the array from PyArrow
    pyarrow_array.call_method1(
        "_export_to_c",
        (array_ptr as Py_uintptr_t, schema_ptr as Py_uintptr_t),
    )?;

    // Import the array into Polars
    let polars_arrow_array = unsafe {
        let field = ffi::import_field_from_c(schema_box.as_ref()).unwrap();

        ffi::import_array_from_c(*array_box, field.dtype).unwrap()
    };

    Ok(polars_arrow_array)
}

pub fn pyarrow_array_from_polars_arrow_array<'a>(
    pyarrow: &Bound<'a, PyModule>,
    polars_arrow_array: Box<dyn Array>,
    polars_arrow_field: &Field,
) -> PyResult<Bound<'a, PyAny>> {
    // Export the array
    let schema = Box::new(ffi::export_field_to_c(polars_arrow_field));
    let array_box = Box::new(ffi::export_array_to_c(polars_arrow_array));

    // Make pointers to the boxes
    let schema_ptr: *const ffi::ArrowSchema = &*schema;
    let array_ptr: *const ffi::ArrowArray = &*array_box;

    // Import the array
    let pyarrow_array = pyarrow.getattr("Array")?.call_method1(
        "_import_from_c",
        (array_ptr as Py_uintptr_t, schema_ptr as Py_uintptr_t),
    )?;

    Ok(pyarrow_array)
}

pub fn record_batches_from_polars_arrow_record_batch<'a>(
    pyarrow: &Bound<'a, PyModule>,
    record_batch: RecordBatchT<Box<dyn Array>>,
) -> PyResult<Bound<'a, PyAny>> {
    let mut arrow_arrays = Vec::with_capacity(record_batch.width());

    for (array, field) in record_batch
        .columns()
        .iter()
        .zip(record_batch.schema().iter_values())
    {
        let pyarrow_array = pyarrow_array_from_polars_arrow_array(pyarrow, array.clone(), field)?;

        arrow_arrays.push(pyarrow_array.unbind());
    }

    let arrow_schema = Box::new(ffi::export_field_to_c(&Field {
        name: PlSmallStr::EMPTY,
        dtype: ArrowDataType::Struct(record_batch.schema().iter_values().cloned().collect()),
        is_nullable: false,
        metadata: None,
    }));
    let arrow_schema_ptr: *const ffi::ArrowSchema = &*arrow_schema;

    let pyarrow_schema = pyarrow
        .getattr("Schema")?
        .call_method1("_import_from_c", (arrow_schema_ptr as Py_uintptr_t,))?;
    let pyarrow_record_batch = pyarrow.getattr("RecordBatch")?.call_method1(
        "from_arrays",
        (arrow_arrays, pyarrow.py().None(), pyarrow_schema),
    )?;

    Ok(pyarrow_record_batch)
}
