__all__ = ["Function", "function_by_name"]

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, Union
from typing_extensions import ParamSpec  # Not present in Python 3.9

import numpy as np
import polars as pl

from ..exceptions import NotSameError

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class Function(Generic[P, R]):
    name: str
    implementation: Callable[P, R]


def polars_same(args):
    x = args[0]
    if x.n_unique() == 0:
        return pl.Series([], dtype=x.dtype)
    elif x.n_unique() == 1:
        return pl.Series([x[0]], dtype=x.dtype)
    else:
        raise NotSameError(x.unique().to_list())


def has_null(x: Union[pl.Expr, float]):
    if isinstance(x, float):
        return False
    elif isinstance(x, pl.Series):
        return x.is_null().any()


def polars_interp(args):
    x, xp, fp = args

    if has_null(x) or has_null(xp) or has_null(fp):
        return pl.Series(values=[None], dtype=pl.Float64)

    if len(x) == 1:
        # Polars does not support scalars
        # Assume all length-1 vectors are scalars
        x = x[0]

    return pl.Series(values=[np.interp(x, xp, fp)], dtype=pl.Float64)


built_in_functions: list[Function[Any, Any]] = [
    # Constant
    Function("n", lambda: pl.count()),  # https://stackoverflow.com/a/71644903/1485877
    Function("row_index0", lambda: pl.int_range(0, pl.count())),
    Function("row_index1", lambda: pl.int_range(1, pl.count() + 1)),
    # Numeric -> numeric elementwise
    Function("abs", lambda x: x.abs()),
    Function("sqrt", lambda x: x.sqrt()),
    Function("log", lambda x: x.log()),
    Function("log2", lambda x: x.log(2)),
    Function("log10", lambda x: x.log10()),
    Function("exp", lambda x: x.exp()),
    Function("pow", lambda x, y: x**y),
    Function("sin", lambda x: x.sin()),
    Function("cos", lambda x: x.cos()),
    Function("tan", lambda x: x.tan()),
    Function("arcsin", lambda x: x.arcsin()),
    Function("arccos", lambda x: x.arccos()),
    Function("arctan", lambda x: x.arctan()),
    Function("floor", lambda x: x.floor()),
    Function("ceil", lambda x: x.ceil()),
    # Numeric -> boolean elementwise
    Function("is_null", lambda x: x.is_null()),
    Function("is_nan", lambda x: x.is_nan()),
    Function("is_finite", lambda x: x.is_finite()),
    # Casting elementwise
    Function("to_boolean", lambda x: x.cast(pl.Boolean)),
    Function("to_integer", lambda x: x.cast(pl.Int64)),
    Function("to_float", lambda x: x.cast(pl.Float64)),
    Function("to_string", lambda x: x.cast(pl.Utf8)),
    # Other elementwise
    Function(
        "if_else",
        lambda condition, true, false=None: pl.when(condition).then(true).otherwise(false),
    ),
    # Numeric -> numeric reduction
    Function("std", lambda x: pl.when(x.is_null().any()).then(None).otherwise(x.std())),
    Function("var", lambda x: pl.when(x.is_null().any()).then(None).otherwise(x.var())),
    Function("max", lambda x: pl.when(x.is_null().any()).then(None).otherwise(x.max())),
    Function("min", lambda x: pl.when(x.is_null().any()).then(None).otherwise(x.min())),
    Function("sum", lambda x: pl.when(x.is_null().any()).then(None).otherwise(x.sum())),
    Function("mean", lambda x: pl.when(x.is_null().any()).then(None).otherwise(x.mean())),
    Function("median", lambda x: pl.when(x.is_null().any()).then(None).otherwise(x.median())),
    Function(
        "quantile",
        lambda x, quantile: pl.when(x.is_null().any())
        .then(None)
        .otherwise(x.quantile(pl.select(quantile).item(), interpolation="linear")),
    ),  # https://stackoverflow.com/a/71721580/
    Function(
        "trapz",
        lambda x, y: pl.when(x.is_null().any().or_(y.is_null().any()))
        .then(None)
        .otherwise(0.5 * ((x - x.shift()) * (y + y.shift())).sum()),
    ),  # https://github.com/pola-rs/polars/issues/3043
    Function(
        "interp",
        lambda x, xp, fp: pl.map_groups(
            exprs=[x, xp, fp],
            function=polars_interp,
        ),
    ),  # https://stackoverflow.com/a/69585269/
    # Boolean -> boolean reduction
    Function("any", lambda x: x.any(ignore_nulls=False)),
    Function("all", lambda x: x.all(ignore_nulls=False)),
    # Any -> any reduction
    # Function("mode", lambda x: x.mode()),  # Not type stable  # noqa: ERA001
    Function("first", lambda x: x.first()),
    Function("last", lambda x: x.last()),
    Function("same", lambda x: pl.map_groups(exprs=[x], function=polars_same)),
]

function_by_name: dict[str, Function[Any, Any]] = {x.name: x for x in built_in_functions}
