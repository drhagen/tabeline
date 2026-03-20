use crate::data_type::DataType;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum LiteralType {
    Whole(u64),
    Integer(i64),
    Float(f64),
}

impl Eq for LiteralType {}

impl std::hash::Hash for LiteralType {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        std::mem::discriminant(self).hash(state);
        match self {
            LiteralType::Whole(v) => v.hash(state),
            LiteralType::Integer(v) => v.hash(state),
            LiteralType::Float(v) => v.to_bits().hash(state),
        }
    }
}

impl LiteralType {
    pub fn data_type(self) -> DataType {
        match self {
            LiteralType::Whole(_) => DataType::Whole64,
            LiteralType::Integer(_) => DataType::Integer64,
            LiteralType::Float(_) => DataType::Float64,
        }
    }

    pub fn is_whole(self) -> bool {
        matches!(self, LiteralType::Whole(_))
    }

    pub fn is_float(self) -> bool {
        matches!(self, LiteralType::Float(_))
    }

    pub fn minimum_data_type(self) -> DataType {
        match self {
            LiteralType::Whole(v) => {
                if v <= u8::MAX as u64 {
                    DataType::Whole8
                } else if v <= u16::MAX as u64 {
                    DataType::Whole16
                } else if v <= u32::MAX as u64 {
                    DataType::Whole32
                } else {
                    DataType::Whole64
                }
            }
            LiteralType::Integer(v) => {
                if v >= i8::MIN as i64 && v <= i8::MAX as i64 {
                    DataType::Integer8
                } else if v >= i16::MIN as i64 && v <= i16::MAX as i64 {
                    DataType::Integer16
                } else if v >= i32::MIN as i64 && v <= i32::MAX as i64 {
                    DataType::Integer32
                } else {
                    DataType::Integer64
                }
            }
            LiteralType::Float(_) => DataType::Float64,
        }
    }

    pub fn to_signed(self) -> LiteralType {
        match self {
            LiteralType::Whole(v) => LiteralType::Integer(v as i64),
            other => other,
        }
    }

    pub fn negate(self) -> LiteralType {
        match self {
            LiteralType::Whole(v) => LiteralType::Integer(-(v as i64)),
            LiteralType::Integer(v) => LiteralType::Integer(-v),
            LiteralType::Float(v) => LiteralType::Float(-v),
        }
    }

    pub fn to_float(self) -> LiteralType {
        match self {
            LiteralType::Whole(v) => LiteralType::Float(v as f64),
            LiteralType::Integer(v) => LiteralType::Float(v as f64),
            LiteralType::Float(_) => self,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ExpressionType {
    Scalar(DataType),
    Array(DataType),
    Literal(LiteralType),
}

impl ExpressionType {
    pub fn data_type(self) -> DataType {
        match self {
            ExpressionType::Scalar(dt) => dt,
            ExpressionType::Array(dt) => dt,
            ExpressionType::Literal(lt) => lt.data_type(),
        }
    }

    pub fn with_data_type(self, dt: DataType) -> ExpressionType {
        match self {
            ExpressionType::Scalar(_) | ExpressionType::Literal(_) => ExpressionType::Scalar(dt),
            ExpressionType::Array(_) => ExpressionType::Array(dt),
        }
    }

    pub fn to_float(self) -> ExpressionType {
        match self {
            ExpressionType::Literal(lt) => ExpressionType::Literal(lt.to_float()),
            _ => self.with_data_type(self.data_type().to_float()),
        }
    }

    pub fn to_signed(self) -> ExpressionType {
        match self {
            ExpressionType::Scalar(dt) => ExpressionType::Scalar(dt.to_signed()),
            ExpressionType::Array(dt) => ExpressionType::Array(dt.to_signed()),
            ExpressionType::Literal(lt) => ExpressionType::Literal(lt.to_signed()),
        }
    }

    pub fn is_scalar(self) -> bool {
        matches!(self, ExpressionType::Scalar(_) | ExpressionType::Literal(_))
    }

    pub fn is_array(self) -> bool {
        matches!(self, ExpressionType::Array(_))
    }

    pub fn is_literal(self) -> bool {
        matches!(self, ExpressionType::Literal(_))
    }
}
