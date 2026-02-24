mod branch;
mod convert;
mod elementwise_extrema;
mod finite;
mod interp;
mod item;
mod log;
mod logical;
mod n;
mod power;
mod reduction_extrema;
mod round;
mod row_index;
mod same;
mod sign;
mod statistics;
mod trapz;
mod trigonometry;

pub use branch::IfElse;
pub use convert::{ToBoolean, ToFloat, ToInteger, ToString};
pub use elementwise_extrema::{PMax, PMin};
pub use finite::{IsFinite, IsNan, IsNull};
pub use interp::Interp;
pub use item::{First, Last};
pub use log::{Log, Log10, Log2};
pub use logical::{All, Any};
pub use n::N;
pub use power::{Exp, Pow, Sqrt};
pub use reduction_extrema::{Max, Min};
pub use round::{Ceil, Floor};
pub use row_index::{RowIndex0, RowIndex1};
pub use same::Same;
pub use sign::Abs;
pub use statistics::{Mean, Median, Quantile, Std, Sum, Var};
pub use trapz::Trapz;
pub use trigonometry::{ArcCos, ArcSin, ArcTan, Cos, Sin, Tan};

use crate::expression::Expression;
use crate::typed_expression::{DataFrameType, Function, ValidationError};
use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::sync::Arc;

type FunctionValidator =
    fn(Vec<Arc<Expression>>, &DataFrameType) -> Result<Arc<dyn Function>, ValidationError>;

static FUNCTION_REGISTRY: Lazy<HashMap<&'static str, FunctionValidator>> = Lazy::new(|| {
    let mut map = HashMap::new();

    map.insert("sqrt", Sqrt::validate as FunctionValidator);
    map.insert("exp", Exp::validate as FunctionValidator);
    map.insert("pow", Pow::validate as FunctionValidator);
    map.insert("abs", Abs::validate as FunctionValidator);
    map.insert("log", Log::validate as FunctionValidator);
    map.insert("log2", Log2::validate as FunctionValidator);
    map.insert("log10", Log10::validate as FunctionValidator);
    map.insert("ceil", Ceil::validate as FunctionValidator);
    map.insert("floor", Floor::validate as FunctionValidator);
    map.insert("sin", Sin::validate as FunctionValidator);
    map.insert("cos", Cos::validate as FunctionValidator);
    map.insert("tan", Tan::validate as FunctionValidator);
    map.insert("arcsin", ArcSin::validate as FunctionValidator);
    map.insert("arccos", ArcCos::validate as FunctionValidator);
    map.insert("arctan", ArcTan::validate as FunctionValidator);
    map.insert("is_finite", IsFinite::validate as FunctionValidator);
    map.insert("is_nan", IsNan::validate as FunctionValidator);
    map.insert("is_null", IsNull::validate as FunctionValidator);
    map.insert("to_boolean", ToBoolean::validate as FunctionValidator);
    map.insert("to_float", ToFloat::validate as FunctionValidator);
    map.insert("to_integer", ToInteger::validate as FunctionValidator);
    map.insert("to_string", ToString::validate as FunctionValidator);
    map.insert("if_else", IfElse::validate as FunctionValidator);
    map.insert("interp", Interp::validate as FunctionValidator);
    map.insert("first", First::validate as FunctionValidator);
    map.insert("last", Last::validate as FunctionValidator);
    map.insert("all", All::validate as FunctionValidator);
    map.insert("any", Any::validate as FunctionValidator);
    map.insert("n", N::validate as FunctionValidator);
    map.insert("pmax", PMax::validate as FunctionValidator);
    map.insert("pmin", PMin::validate as FunctionValidator);
    map.insert("max", Max::validate as FunctionValidator);
    map.insert("min", Min::validate as FunctionValidator);
    map.insert("row_index0", RowIndex0::validate as FunctionValidator);
    map.insert("row_index1", RowIndex1::validate as FunctionValidator);
    map.insert("same", Same::validate as FunctionValidator);
    map.insert("mean", Mean::validate as FunctionValidator);
    map.insert("median", Median::validate as FunctionValidator);
    map.insert("quantile", Quantile::validate as FunctionValidator);
    map.insert("std", Std::validate as FunctionValidator);
    map.insert("sum", Sum::validate as FunctionValidator);
    map.insert("var", Var::validate as FunctionValidator);
    map.insert("trapz", Trapz::validate as FunctionValidator);

    map
});

pub fn validate_function(
    name: &str,
    arguments: Vec<Arc<Expression>>,
    df_type: &DataFrameType,
) -> Result<Arc<dyn Function>, ValidationError> {
    let validator =
        FUNCTION_REGISTRY
            .get(name)
            .ok_or_else(|| ValidationError::UnknownFunction {
                name: name.to_string(),
                available: FUNCTION_REGISTRY.keys().map(|&s| s.to_string()).collect(),
            })?;

    validator(arguments, df_type)
}
