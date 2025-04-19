__all__ = ["to_py_expression"]

from functools import singledispatch

from .._tabeline import PyExpression, functions
from . import ast


@singledispatch
def to_py_expression(expression) -> PyExpression:
    raise NotImplementedError(f"to_py_expression not implemented for {type(expression)}")


@to_py_expression.register
def _(expression: ast.NullLiteral) -> PyExpression:
    return PyExpression.null()


@to_py_expression.register
def _(expression: ast.BooleanLiteral) -> PyExpression:
    return PyExpression.boolean(expression.value)


@to_py_expression.register
def _(expression: ast.IntegerLiteral) -> PyExpression:
    return PyExpression.integer(expression.value)


@to_py_expression.register
def _(expression: ast.FloatLiteral) -> PyExpression:
    return PyExpression.float(expression.value)


@to_py_expression.register
def _(expression: ast.StringLiteral) -> PyExpression:
    return PyExpression.string(expression.value)


@to_py_expression.register
def _(expression: ast.Variable) -> PyExpression:
    return PyExpression.variable(expression.name)


@to_py_expression.register
def _(expression: ast.Positive) -> PyExpression:
    return to_py_expression(expression.content).positive()


@to_py_expression.register
def _(expression: ast.Negative) -> PyExpression:
    return to_py_expression(expression.content).negative()


@to_py_expression.register
def _(expression: ast.Add) -> PyExpression:
    return to_py_expression(expression.left).add(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.Subtract) -> PyExpression:
    return to_py_expression(expression.left).subtract(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.Multiply) -> PyExpression:
    return to_py_expression(expression.left).multiply(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.Divide) -> PyExpression:
    return to_py_expression(expression.left).true_divide(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.FloorDivide) -> PyExpression:
    return to_py_expression(expression.left).floor_divide(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.Call) -> PyExpression:
    return getattr(functions, expression.name)(*map(to_py_expression, expression.arguments))


@to_py_expression.register
def _(expression: ast.Mod) -> PyExpression:
    return to_py_expression(expression.left).modulo(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.Power) -> PyExpression:
    return to_py_expression(expression.left).power(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.Equal) -> PyExpression:
    return to_py_expression(expression.left).equal(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.NotEqual) -> PyExpression:
    return to_py_expression(expression.left).not_equal(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.GreaterThan) -> PyExpression:
    return to_py_expression(expression.left).greater_than(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.LessThan) -> PyExpression:
    return to_py_expression(expression.left).less_than(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.GreaterThanOrEqual) -> PyExpression:
    return to_py_expression(expression.left).greater_than_or_equal(
        to_py_expression(expression.right)
    )


@to_py_expression.register
def _(expression: ast.LessThanOrEqual) -> PyExpression:
    return to_py_expression(expression.left).less_than_or_equal(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.Not) -> PyExpression:
    return to_py_expression(expression.content).not_()


@to_py_expression.register
def _(expression: ast.And) -> PyExpression:
    return to_py_expression(expression.left).and_(to_py_expression(expression.right))


@to_py_expression.register
def _(expression: ast.Or) -> PyExpression:
    return to_py_expression(expression.left).or_(to_py_expression(expression.right))
