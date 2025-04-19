use polars::prelude::*;

pub const DUMMY_NAME: &str = "_dummy";

pub fn dummy_column(height: usize) -> Column {
    // WORKAROUND: Polars loses height information when a data frame has no columns.
    // This is a column whose values do not matter, but can be inserted into a
    // data frame to ensure that there is always at least one column.
    Column::new_scalar(
        DUMMY_NAME.into(),
        Scalar::new(DataType::Null, AnyValue::Null),
        height,
    )
}

pub fn prepend_dummy_column(df: DataFrame) -> DataFrame {
    DataFrame::new(vec![dummy_column(df.height())])
        .unwrap()
        .hstack(df.get_columns())
        .unwrap()
}
