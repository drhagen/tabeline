use crate::data_type::DataType;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ExpressionType {
    Scalar(DataType),
    Array(DataType),
}

impl ExpressionType {
    pub fn data_type(self) -> DataType {
        match self {
            ExpressionType::Scalar(dt) => dt,
            ExpressionType::Array(dt) => dt,
        }
    }

    pub fn with_data_type(self, dt: DataType) -> ExpressionType {
        match self {
            ExpressionType::Scalar(_) => ExpressionType::Scalar(dt),
            ExpressionType::Array(_) => ExpressionType::Array(dt),
        }
    }

    pub fn to_float(self) -> ExpressionType {
        self.with_data_type(self.data_type().to_float())
    }
}
