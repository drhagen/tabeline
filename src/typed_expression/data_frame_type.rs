use crate::data_frame::PyDataFrame;
use crate::data_type::DataType;
use crate::typed_expression::ExpressionType;
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DataFrameType {
    columns: HashMap<String, DataType>,
}

impl DataFrameType {
    pub fn new() -> Self {
        DataFrameType {
            columns: HashMap::new(),
        }
    }

    pub fn from_data_frame(df: &PyDataFrame) -> Self {
        let mut columns = HashMap::new();
        for (name, array) in df.iter_columns() {
            let dtype = DataType::from(array.polars_column.dtype());
            columns.insert(name.to_string(), dtype);
        }
        DataFrameType { columns }
    }

    pub fn column_expression_type(&self, name: &str) -> Option<ExpressionType> {
        self.columns.get(name).map(|dt| ExpressionType::Array(*dt))
    }

    pub fn with_column(mut self, name: String, data_type: DataType) -> Self {
        self.columns.insert(name, data_type);
        self
    }

    pub fn column_names(&self) -> Vec<String> {
        let mut names: Vec<String> = self.columns.keys().cloned().collect();
        names.sort();
        names
    }
}
