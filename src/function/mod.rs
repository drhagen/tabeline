mod branch;
mod convert;
mod extrema;
mod finite;
mod interp;
mod item;
mod log;
mod logical;
mod n;
mod power;
mod round;
mod row_index;
mod same;
mod sign;
mod statistics;
mod trapz;
mod trigonometry;

pub use branch::IfElse;
pub use convert::{ToBoolean, ToFloat, ToInteger, ToString};
pub use extrema::{Max, Min};
pub use finite::{IsFinite, IsNan, IsNull};
pub use interp::Interp;
pub use item::{First, Last};
pub use log::{Log, Log10, Log2};
pub use logical::{All, Any};
pub use n::N;
pub use power::{Exp, Pow, Sqrt};
pub use round::{Ceil, Floor};
pub use row_index::{RowIndex0, RowIndex1};
pub use same::Same;
pub use sign::Abs;
pub use statistics::{Mean, Median, Quantile, Std, Sum, Var};
pub use trapz::Trapz;
pub use trigonometry::{ArcCos, ArcSin, ArcTan, Cos, Sin, Tan};

use crate::expression::Expression;
use std::{collections::HashMap, fmt::Debug};

pub trait Function: Debug + Sync + Send + FunctionClone {
    fn to_polars(&self) -> polars::lazy::dsl::Expr;
    fn substitute(&self, substitutions: &HashMap<&str, Expression>) -> Box<dyn Function>;
    fn as_any(&self) -> &dyn std::any::Any;
    fn equals(&self, other: &dyn Function) -> bool;
}

pub trait FunctionClone {
    fn clone_box(&self) -> Box<dyn Function>;
}

impl<T> FunctionClone for T
where
    T: 'static + Function + Clone,
{
    fn clone_box(&self) -> Box<dyn Function> {
        Box::new(self.clone())
    }
}

impl PartialEq for dyn Function {
    fn eq(&self, other: &Self) -> bool {
        self.equals(other)
    }
}
