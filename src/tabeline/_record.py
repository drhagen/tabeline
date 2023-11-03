from __future__ import annotations

__all__ = ["Record"]

from typing import Iterator, overload

from ._validation import missing


class Record:
    @overload
    def __init__(self, **items: bool | int | float | str | None):
        pass

    @overload
    def __init__(self, data: dict[str, bool | int | float | str | None], /):
        pass

    def __init__(self, data=missing, /, **items):
        if data is missing:
            self._data = items
        else:
            self._data = data

    @staticmethod
    def from_dict(data: dict[str, bool | int | float | str | None], /) -> Record:
        return Record(data)

    def to_dict(self) -> dict[str, bool | int | float | str | None]:
        return self._data

    def __eq__(self, other: object) -> bool:
        # Cannot add `strict=True` to `zip` and still run on Python 3.9
        if isinstance(other, Record):
            return len(self) == len(other) and all(
                item == other_item
                for item, other_item in zip(self._data.items(), other._data.items())
            )
        elif isinstance(other, dict):
            return len(self) == len(other) and all(
                item == other_item for item, other_item in zip(self._data.items(), other.items())
            )
        return NotImplemented

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: str) -> bool | int | float | str:
        return self._data[key]

    def items(self) -> Iterator[str, bool | int | float | str]:
        yield from self._data.items()

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return f"Record({', '.join(f'{key}={value!r}' for key, value in self._data.items())})"
