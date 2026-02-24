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
}
