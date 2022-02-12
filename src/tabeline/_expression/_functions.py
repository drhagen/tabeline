__all__ = ["Function", "function_by_name"]

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar
from typing_extensions import ParamSpec  # Not present in Python 3.9

import polars as pl

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class Function(Generic[P, R]):
    name: str
    implementation: Callable[P, R]


built_in_functions: list[Function[Any, Any]] = [
    # Constant
    Function("n", lambda: pl.first().count()),  # https://stackoverflow.com/a/71644903/1485877
    Function("row_index0", lambda: pl.arange(0, pl.count())),
    Function("row_index1", lambda: pl.arange(0, pl.count()) + 1),
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
    # Function("arcsin", lambda x: x.arcsin()),  # Decide on name
    # Function("arccos", lambda x: x.arccos()),  # Decide on name
    # Function("arctan", lambda x: x.arctan()),  # Decide on name
    Function("floor", lambda x: x.floor()),
    Function("ceil", lambda x: x.ceil()),
    # Numeric -> boolean elementwise
    Function("is_nan", lambda x: x.is_nan()),
    # Numeric -> numeric reduction
    Function("std", lambda x: x.std()),
    Function("var", lambda x: x.var()),
    Function("max", lambda x: x.max()),
    Function("min", lambda x: x.min()),
    Function("sum", lambda x: x.sum()),
    Function("mean", lambda x: x.mean()),
    Function("median", lambda x: x.median()),
    Function(
        "quantile",
        lambda x, quantile: x.quantile(pl.select(quantile)[0, 0], interpolation="linear"),
    ),
    Function(
        "trapz", lambda x, y: 0.5 * ((x - x.shift()) * (y + y.shift())).sum()
    ),  # https://github.com/pola-rs/polars/issues/3043
    # Boolean -> boolean reduction
    Function("any", lambda x: x.any()),
    Function("all", lambda x: x.all()),
    # Any -> any reduction
    # Function("mode", lambda x: x.mode()),  # Not type stable
    Function("first", lambda x: x.first()),
    Function("last", lambda x: x.last()),
]

function_by_name: dict[str, Function[Any, Any]] = {x.name: x for x in built_in_functions}
