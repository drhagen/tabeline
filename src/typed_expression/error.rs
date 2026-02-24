use crate::data_type::DataType;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ValidationError {
    UnknownVariable {
        name: String,
        available: Vec<String>,
    },
    IncompatibleTypes {
        operation: String,
        left_type: DataType,
        right_type: DataType,
    },
    IncomparableTypes {
        left_type: DataType,
        right_type: DataType,
    },
    FunctionArgumentType {
        function: String,
        parameter: String,
        expected: String,
        actual: DataType,
    },
    FunctionArgumentCount {
        function: String,
        expected: usize,
        actual: usize,
    },
    TypeMismatch {
        operation: String,
        expected: DataType,
        actual: DataType,
    },
    NumericTypeNotSatisfied {
        operation: String,
        actual: DataType,
    },
    FunctionNotImplemented {
        function: String,
    },
    UnknownFunction {
        name: String,
        available: Vec<String>,
    },
}
