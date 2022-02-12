__all__ = ["substitute"]

from functools import singledispatch

from . import ast


@singledispatch
def substitute(self: ast.Expression, variables: dict[str, ast.Expression]) -> ast.Expression:
    raise NotImplementedError()


@substitute.register(ast.NullLiteral)
def substitute_null_literal(
    self: ast.Expression, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return self


@substitute.register(ast.BooleanLiteral)
def substitute_boolean_literal(
    self: ast.BooleanLiteral, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return self


@substitute.register(ast.IntegerLiteral)
def substitute_integer_literal(
    self: ast.IntegerLiteral, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return self


@substitute.register(ast.FloatLiteral)
def substitute_float_literal(
    self: ast.FloatLiteral, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return self


@substitute.register(ast.StringLiteral)
def substitute_string_literal(
    self: ast.StringLiteral, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return self


@substitute.register(ast.Variable)
def substitute_variable(
    self: ast.Variable, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return variables.get(self.name, self)


@substitute.register(ast.Positive)
def substitute_positive(
    self: ast.Positive, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return ast.Positive(substitute(self.content, variables))


@substitute.register(ast.Negative)
def substitute_negative(
    self: ast.Negative, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return ast.Negative(substitute(self.content, variables))


@substitute.register(ast.Add)
def substitute_add(self: ast.Add, variables: dict[str, ast.Expression]) -> ast.Expression:
    return ast.Add(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.Subtract)
def substitute_subtract(
    self: ast.Subtract, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return ast.Subtract(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.Multiply)
def substitute_multiply(
    self: ast.Multiply, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return ast.Multiply(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.Divide)
def substitute_divide(self: ast.Divide, variables: dict[str, ast.Expression]) -> ast.Expression:
    return ast.Divide(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.Mod)
def substitute_mod(self: ast.Mod, variables: dict[str, ast.Expression]) -> ast.Expression:
    return ast.Mod(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.Power)
def substitute_power(self: ast.Power, variables: dict[str, ast.Expression]) -> ast.Expression:
    return ast.Power(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.Call)
def substitute_call(self: ast.Call, variables: dict[str, ast.Expression]) -> ast.Expression:
    return ast.Call(self.name, [substitute(argument, variables) for argument in self.arguments])


@substitute.register(ast.Equal)
def substitute_equal(self: ast.Equal, variables: dict[str, ast.Expression]) -> ast.Expression:
    return ast.Equal(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.NotEqual)
def substitute_not_equal(
    self: ast.NotEqual, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return ast.NotEqual(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.GreaterThanOrEqual)
def substitute_greater_than_or_equal(
    self: ast.GreaterThanOrEqual, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return ast.GreaterThanOrEqual(
        substitute(self.left, variables), substitute(self.right, variables)
    )


@substitute.register(ast.LessThanOrEqual)
def substitute_less_than_or_equal(
    self: ast.LessThanOrEqual, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return ast.LessThanOrEqual(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.GreaterThan)
def substitute_greater_than(
    self: ast.GreaterThan, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return ast.GreaterThan(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.LessThan)
def substitute_less_than(
    self: ast.LessThan, variables: dict[str, ast.Expression]
) -> ast.Expression:
    return ast.LessThan(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.Not)
def substitute_not(self: ast.Not, variables: dict[str, ast.Expression]) -> ast.Expression:
    return ast.Not(substitute(self.content, variables))


@substitute.register(ast.And)
def substitute_and(self: ast.And, variables: dict[str, ast.Expression]) -> ast.Expression:
    return ast.And(substitute(self.left, variables), substitute(self.right, variables))


@substitute.register(ast.Or)
def substitute_or(self: ast.Or, variables: dict[str, ast.Expression]) -> ast.Expression:
    return ast.Or(substitute(self.left, variables), substitute(self.right, variables))
