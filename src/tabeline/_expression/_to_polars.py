__all__ = ["to_polars"]

from functools import singledispatch

import polars as pl

from . import ast
from ._functions import function_by_name


@singledispatch
def to_polars(self: ast.Expression) -> pl.Expr:
    raise NotImplementedError()


@to_polars.register(ast.NullLiteral)
def to_polars_null_literal(self: ast.NullLiteral) -> pl.Expr:
    return pl.lit(None)


@to_polars.register(ast.BooleanLiteral)
def to_polars_boolean_literal(self: ast.BooleanLiteral) -> pl.Expr:
    return pl.lit(self.value, dtype=pl.datatypes.Boolean)


@to_polars.register(ast.IntegerLiteral)
def to_polars_integer_literal(self: ast.IntegerLiteral) -> pl.Expr:
    return pl.lit(self.value, dtype=pl.datatypes.Int64)


@to_polars.register(ast.FloatLiteral)
def to_polars_float_literal(self: ast.FloatLiteral) -> pl.Expr:
    return pl.lit(self.value, dtype=pl.datatypes.Float64)


@to_polars.register(ast.StringLiteral)
def to_polars_string_literal(self: ast.StringLiteral) -> pl.Expr:
    return pl.lit(self.value, dtype=pl.datatypes.Utf8)


@to_polars.register(ast.Variable)
def to_polars_variable(self: ast.Variable) -> pl.Expr:
    return pl.col(self.name)


@to_polars.register(ast.Positive)
def to_polars_positive(self: ast.Positive) -> pl.Expr:
    return to_polars(self.content)


@to_polars.register(ast.Negative)
def to_polars_negative(self: ast.Negative) -> pl.Expr:
    return -to_polars(self.content)


@to_polars.register(ast.Add)
def to_polars_add(self: ast.Add) -> pl.Expr:
    return to_polars(self.left) + to_polars(self.right)


@to_polars.register(ast.Subtract)
def to_polars_subtract(self: ast.Subtract) -> pl.Expr:
    return to_polars(self.left) - to_polars(self.right)


@to_polars.register(ast.Multiply)
def to_polars_multiply(self: ast.Multiply) -> pl.Expr:
    return to_polars(self.left) * to_polars(self.right)


@to_polars.register(ast.Divide)
def to_polars_divide(self: ast.Divide) -> pl.Expr:
    return to_polars(self.left) / to_polars(self.right)


@to_polars.register(ast.Mod)
def to_polars_mod(self: ast.Mod) -> pl.Expr:
    return to_polars(self.left) % to_polars(self.right)


@to_polars.register(ast.Power)
def to_polars_power(self: ast.Power) -> pl.Expr:
    return to_polars(self.left) ** to_polars(self.right)


@to_polars.register(ast.Call)
def to_polars_call(self: ast.Call) -> pl.Expr:
    function = function_by_name[self.name]
    return function.implementation(*map(to_polars, self.arguments))


@to_polars.register(ast.Equal)
def to_polars_equal(self: ast.Equal) -> pl.Expr:
    return to_polars(self.left) == to_polars(self.right)


@to_polars.register(ast.NotEqual)
def to_polars_not_equal(self: ast.NotEqual) -> pl.Expr:
    return to_polars(self.left) != to_polars(self.right)


@to_polars.register(ast.GreaterThanOrEqual)
def to_polars_greater_than_or_equal(self: ast.GreaterThanOrEqual) -> pl.Expr:
    return to_polars(self.left) >= to_polars(self.right)


@to_polars.register(ast.LessThanOrEqual)
def to_polars_less_than_or_equal(self: ast.LessThanOrEqual) -> pl.Expr:
    return to_polars(self.left) <= to_polars(self.right)


@to_polars.register(ast.GreaterThan)
def to_polars_greater_than(self: ast.GreaterThan) -> pl.Expr:
    return to_polars(self.left) > to_polars(self.right)


@to_polars.register(ast.LessThan)
def to_polars_less_than(self: ast.LessThan) -> pl.Expr:
    return to_polars(self.left) < to_polars(self.right)


@to_polars.register(ast.Not)
def to_polars_not(self: ast.Not) -> pl.Expr:
    return ~to_polars(self.content)


@to_polars.register(ast.And)
def to_polars_and(self: ast.And) -> pl.Expr:
    return to_polars(self.left) & to_polars(self.right)


@to_polars.register(ast.Or)
def to_polars_or(self: ast.Or) -> pl.Expr:
    return to_polars(self.left) | to_polars(self.right)
