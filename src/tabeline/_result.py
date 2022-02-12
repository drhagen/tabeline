from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, NoReturn, TypeVar

Value = TypeVar("Value")
Error = TypeVar("Error", bound=Exception)


class Result(Generic[Value, Error]):
    pass

    @abstractmethod
    def or_die(self) -> Value:
        pass


@dataclass(frozen=True)
class Success(Result[Value, NoReturn]):
    value: Value

    def or_die(self) -> Value:
        return self.value


@dataclass(frozen=True)
class Failure(Result[NoReturn, Error]):
    error: Error

    def or_die(self) -> Value:
        raise self.error
