from __future__ import annotations

__all__ = [
    "Expression",
    "NullLiteral",
    "BooleanLiteral",
    "IntegerLiteral",
    "FloatLiteral",
    "StringLiteral",
    "Variable",
    "Positive",
    "Negative",
    "Add",
    "Subtract",
    "Multiply",
    "Divide",
    "Mod",
    "Power",
    "Call",
    "Equal",
    "NotEqual",
    "GreaterThan",
    "LessThan",
    "GreaterThanOrEqual",
    "LessThanOrEqual",
    "Not",
    "And",
    "Or",
]

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .._result import Result

if TYPE_CHECKING:
    from ._parser import ParseError


class Expression:
    @staticmethod
    def parse(text: str) -> Result[Expression, ParseError]:
        from ._parser import parse_expression

        return parse_expression(text)


@dataclass(frozen=True)
class NullLiteral(Expression):
    pass


@dataclass(frozen=True)
class BooleanLiteral(Expression):
    value: bool


@dataclass(frozen=True)
class IntegerLiteral(Expression):
    value: int


@dataclass(frozen=True)
class FloatLiteral(Expression):
    value: float


@dataclass(frozen=True)
class StringLiteral(Expression):
    value: str


@dataclass(frozen=True)
class Variable(Expression):
    name: str


@dataclass(frozen=True)
class Positive(Expression):
    content: Expression


@dataclass(frozen=True)
class Negative(Expression):
    content: Expression


@dataclass(frozen=True)
class Add(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Subtract(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Multiply(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Divide(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Mod(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Power(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Call(Expression):
    name: str
    arguments: list[Expression]


@dataclass(frozen=True)
class Equal(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class NotEqual(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class GreaterThanOrEqual(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class LessThanOrEqual(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class GreaterThan(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class LessThan(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Not(Expression):
    content: Expression


@dataclass(frozen=True)
class And(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Or(Expression):
    left: Expression
    right: Expression
