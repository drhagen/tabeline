---
icon: material/code-brackets
---

# Indexing

Indexing is the use of the `df[..., ...]` syntax to extract values from the data frame. Two arguments are always required, the row index followed by the column index. The returned type depends on which arguments are scalars or slices. This operator ignores any group levels that may be present.


## `df[row_index: int, column_index: str]`

Indexing with a scalar row index and a scalar column index returns a scalar value. The returned type is a Python type, `bool`, `int`, `float`, or `str`.

```python
from tabeline import DataFrame

df = DataFrame(
    book=["The Hobbit", "The Fellowship of the Ring", "The Two Towers", "The Return of the King"],
    year=[1937, 1954, 1954, 1955],
    word_count=[95356, 187790, 156198, 137115],
)

assert df[2, "book"] == "The Two Towers"
```


## `df[row_index: int, column_index: slice | Sequence[str]]`

If only the row index is a scalar, indexing returns a `tabeline.Record`. Functionally, a `Record` is an ordered dict.

A `Record` can be iterated over or indexed further. Each key is a string, and each value is a Python type, `bool`, `int`, `float`, `str`, or `None`. The underlying data types are lost when a `Record` is created.

A `slice(None)` (i.e. `:`, all columns) is the only slice allowed. Sliced `str` ranges are not supported. To select a subset of columns, list them as a sequence of strings.

```python
from tabeline import DataFrame

df = DataFrame(
    book=["The Hobbit", "The Fellowship of the Ring", "The Two Towers", "The Return of the King"],
    year=[1937, 1954, 1954, 1955],
    word_count=[95356, 187790, 156198, 137115],
)

assert df[2, :] == Record(book="The Two Towers", year=1954, word_count=156198)
assert df[2, :]["book"] == "The Two Towers"
```


## `df[row_index: slice | Sequence[int], column_index: str]`

If only the column index is a scalar, indexing returns a `tabeline.Array`. Functionally, an `Array` is a list.

Normal `slice`s are permitted on the row index and behave as expected. Selecting specific rows with a sequennce of integers is also allowed.

```python
from tabeline import DataFrame

df = DataFrame(
    book=["The Hobbit", "The Fellowship of the Ring", "The Two Towers", "The Return of the King"],
    year=[1937, 1954, 1954, 1955],
    word_count=[95356, 187790, 156198, 137115],
)

assert df[:, "word_count"] == Array(95356, 187790, 156198, 137115)
assert df[:, "word_count"][2] == 156198
```

### `Array`

Each `Array` has a given data type that restricts the possible values that the elements may have. The data type can be accessed via the `Array.data_type` attribute, which returns a member of the `tabeline.DataType` enum. All the elements in a given `Array` are instances of that type or are null. Tabeline currently has no scalar values so getting a lone instance of the data type in Python is not possible. Extracting a single element from an `Array` or `DataFrame` returns an object with one of these basic Python types: `bool`, `int`, `float`, `str`, or `None`.

The possible data types are listed below. The `in` column in the table below indicate which Python type is converted to that data type. The `out` column indicates with Python type is returned when extracting a value from that data type.

| DataType  | in    | out   |
|-----------|-------|-------|
| Boolean   | bool  | bool  |
| Integer8  |       | int   |
| Integer16 |       | int   |
| Integer32 |       | int   |
| Integer64 | int   | int   |
| Whole8    |       | int   |
| Whole16   |       | int   |
| Whole32   |       | int   |
| Whole64   |       | int   |
| Float32   |       | float |
| Float64   | float | float |
| String    | str   | str   |
| Nothing   |       |       |


## `df[row_index: slice | Sequence[int], column_index: slice | Sequence[str]]`

Slicing both the row index and the column index returns another `tabeline.DataFrame`.

The resulting `DataFrame` has no group levels regardless of the parent.

```python
from tabeline import DataFrame

df = DataFrame(
    book=["The Hobbit", "The Fellowship of the Ring", "The Two Towers", "The Return of the King"],
    year=[1937, 1954, 1954, 1955],
    word_count=[95356, 187790, 156198, 137115],
)

assert df[1:3, ["book", "year"]] == DataFrame(
    book=["The Fellowship of the Ring", "The Two Towers"],
    year=[1954, 1954],
)
```
