__all__ = ["parse_expression", "ParseError"]

from functools import reduce
from typing import Literal, Union

from parsita import Failure, TextParsers, lit, opt, pred, reg, rep, rep1sep, repsep
from parsita.util import constant, splat

from .. import _result
from . import ast
from .ast import Expression

reserved_names = {"None", "True", "False", "inf", "nan"}


def make_exponent(first: Expression, maybe_second: Union[tuple[()], tuple[Expression]]):
    if len(maybe_second) == 0:
        return first
    else:
        return ast.Power(first, maybe_second[0])


def make_term(first: Expression, rest: list[tuple[Literal["*", "/"], Expression]]) -> Expression:
    value = first
    for op, factor in rest:
        if op == "*":
            value = ast.Multiply(value, factor)
        elif op == "/":
            value = ast.Divide(value, factor)
        elif op == "%":
            value = ast.Mod(value, factor)
        else:
            raise NotImplementedError
    return value


def make_numeric_expression(
    first: Expression, rest: list[tuple[Literal["+", "-"], Expression]]
) -> Expression:
    value = first
    for op, term in rest:
        if op == "+":
            value = ast.Add(value, term)
        elif op == "-":
            value = ast.Subtract(value, term)
        else:
            raise NotImplementedError
    return value


def make_comparison_expression(
    first: Expression, maybe_second: Union[tuple[()], tuple[Expression]]
) -> Expression:
    if len(maybe_second) == 0:
        return first
    else:
        op, second = maybe_second[0]
        if op == "==":
            return ast.Equal(first, second)
        elif op == "!=":
            return ast.NotEqual(first, second)
        elif op == ">=":
            return ast.GreaterThanOrEqual(first, second)
        elif op == "<=":
            return ast.LessThanOrEqual(first, second)
        elif op == ">":
            return ast.GreaterThan(first, second)
        elif op == "<":
            return ast.LessThan(first, second)
        else:
            raise NotImplementedError


class ExpressionParser(TextParsers):
    name = pred(reg(r"[A-Za-z_][A-Za-z_0-9]*"), lambda x: x not in reserved_names, "non-keyword")

    # Atoms
    null = lit("None") > constant(ast.NullLiteral())

    true = lit("True") > constant(ast.BooleanLiteral(True))
    false = lit("False") > constant(ast.BooleanLiteral(False))
    boolean_literal = true | false

    float_literal = reg(r"\d+((\.\d+([Ee][+-]?\d+)?)|((\.\d+)?[Ee][+-]?\d+))") | reg(
        r"\binf\b"
    ) | reg(r"\bnan\b") > (lambda x: ast.FloatLiteral(float(x)))

    integer_literal = reg(r"\d+") > (lambda x: ast.IntegerLiteral(int(x)))

    string_literal = reg(r"'[^']*'") > (lambda x: ast.StringLiteral(x[1:-1]))

    variable = name > ast.Variable

    function = name & "(" >> repsep(expression, ",") << ")" > splat(ast.Call)

    parentheses = "(" >> expression << ")"

    atom = (
        null
        | boolean_literal
        | float_literal
        | integer_literal
        | string_literal
        | function
        | variable
        | parentheses
    )

    # Numeric operators
    positive = "+" >> factor > ast.Positive
    negative = "-" >> factor > ast.Negative
    exponent = atom & opt("**" >> factor) > splat(make_exponent)
    factor = positive | negative | exponent

    term = factor & rep(lit("*", "/", "%") & factor) > splat(make_term)
    numeric_expression = term & rep(lit("+", "-") & term) > splat(make_numeric_expression)

    # Comparison operators
    comparison_expression = numeric_expression & opt(
        lit("==", "!=", ">=", "<=", ">", "<") & numeric_expression
    ) > splat(make_comparison_expression)

    # Boolean operators
    not_expression = "~" >> unary_boolean > ast.Not

    unary_boolean = not_expression | comparison_expression

    and_expression = rep1sep(unary_boolean, "&") > (lambda x: reduce(ast.And, x))
    expression = rep1sep(and_expression, "|") > (lambda x: reduce(ast.Or, x))


class ParseError(Exception):
    pass


def parse_expression(text: str) -> _result.Result[Expression, ParseError]:
    result = ExpressionParser.expression.parse(text)

    if isinstance(result, Failure):
        return _result.Failure(ParseError(result.message))
    else:
        return _result.Success(result.or_die())
