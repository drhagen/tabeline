---
icon: material/export
---

# Export

`DataFrame`s can be converted into various other formats. These mostly mirror the [creation methods](creation.md).


## `to_dict()`

Convert to dictionary of columns. Each key of the dictionary is a column name, and each value is an `Array` of the column's values.

```python
from tabeline import DataFrame

df = DataFrame(
    name=["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    episode=[4, 5, 6],
    release_year=[1977, 1980, 1983],
)

df.to_dict()
# {
#     'name': Array(['A New Hope', 'The Empire Strikes Back', 'Return of the Jedi']),
#     'episode': Arry([4, 5, 6]),
#     'release_year': Array([1977, 1980, 1983]),
# }
```

See also [`DataFrame.from_dict`](creation.md#dataframefrom_dict).


## `write_csv(filename)`

Write to a CSV file. Each column name is a header, and each row is a row of values.

```python
from tabeline import DataFrame

df = DataFrame(
    name=["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    episode=[4, 5, 6],
    release_year=[1977, 1980, 1983],
)

df.write_csv("star_wars.csv")
```

See also [`DataFrame.read_csv`](creation.md#dataframeread_csv).


## `to_pandas()`

Convert to a Pandas `DataFrame`. This requires that the `pandas` extra is installed (i.e. `pip install tabeline[pandas]`).

```python
from tabeline import DataFrame

df = DataFrame(
    name=["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    episode=[4, 5, 6],
    release_year=[1977, 1980, 1983],
)

df.to_pandas()
#                       name  episode  release_year
# 0               A New Hope        4          1977
# 1  The Empire Strikes Back        5          1980
# 2       Return of the Jedi        6          1983
```

See also [`DataFrame.from_pandas`](creation.md#dataframefrom_pandas).


## `to_polars()`

Convert to a Polars `DataFrame`.

```python
from tabeline import DataFrame

df = DataFrame(
    name=["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    episode=[4, 5, 6],
    release_year=[1977, 1980, 1983],
)

df.to_polars()
# ┌─────────────────────────┬─────────┬──────────────┐
# │ name                    ┆ episode ┆ release_year │
# │ ---                     ┆ ---     ┆ ---          │
# │ str                     ┆ i64     ┆ i64          │
# ╞═════════════════════════╪═════════╪══════════════╡
# │ A New Hope              ┆ 4       ┆ 1977         │
# │ The Empire Strikes Back ┆ 5       ┆ 1980         │
# │ Return of the Jedi      ┆ 6       ┆ 1983         │
# └─────────────────────────┴─────────┴──────────────┘
```

See also [`DataFrame.from_polars`](creation.md#dataframefrom_polars).
