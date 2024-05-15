---
icon: material/filter-remove
---

# Row dropping

The `filter`, `slice0`, `slice1`, `distinct`, and `unique` verbs change which rows are present. The relative order of the rows is unchanged.

## `filter`

Keep the rows for which a given predicate evaluates to true. `filter` takes a single expression, which in the context of the data frame, must evaluate to a boolean column. All rows with a corresponding false value are dropped.

```python
from tabeline import DataFrame

df = DataFrame(
    name=["Alice", "Bob", "Carole", "Mallory"],
    age=[28, 55, 55, 18],
)

df.filter("age == max(age)")
# shape: (2, 2)
# ┌────────┬─────┐
# │ name   ┆ age │
# │ ---    ┆ --- │
# │ str    ┆ i64 │
# ╞════════╪═════╡
# │ Bob    ┆ 55  │
# ├╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
# │ Carole ┆ 55  │
# └────────┴─────┘
```

## `slice0`

Keep only the rows whose 0-based index is listed, and in the order listed.

```python
from tabeline import DataFrame

df = DataFrame(
    id=[1, 2, 3, 4],
    character=["a", "b", "c", "d"],
)

df.slice0([2, 1])
# ┌─────┬───────────┐
# │ id  ┆ character │
# │ --- ┆ ---       │
# │ i64 ┆ str       │
# ╞═════╪═══════════╡
# │ 3   ┆ c         │
# ├╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌┤
# │ 2   ┆ b         │
# └─────┴───────────┘
```

## `slice1`

Keep only the rows whose 1-based index is listed, and in the order listed. This is identical to `slice0` except for the interpretation of the index.

```python
from tabeline import DataFrame

df = DataFrame(
    id=[1, 2, 3, 4],
    character=["a", "b", "c", "d"],
)

df.slice1([2, 1])
# shape: (2, 2)
# ┌─────┬───────────┐
# │ id  ┆ character │
# │ --- ┆ ---       │
# │ i64 ┆ str       │
# ╞═════╪═══════════╡
# │ 2   ┆ b         │
# ├╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌┤
# │ 1   ┆ a         │
# └─────┴───────────┘
```

## `distinct`

Keep the first row for each unique record in the columns whose names are listed.

```python
from tabeline import DataFrame

df = DataFrame(
    given_name=["Alice", "Bob", "Alice", "Alice", "Bob"],
    family_name=["Smith", "Smith", "Smith", "Jones", "Smith"],
    age=[28, 30, 30, 18, 30],
)

df.distinct("given_name", "family_name")
# shape: (3, 3)
# ┌────────────┬─────────────┬─────┐
# │ given_name ┆ family_name ┆ age │
# │ ---        ┆ ---         ┆ --- │
# │ str        ┆ str         ┆ i64 │
# ╞════════════╪═════════════╪═════╡
# │ Alice      ┆ Smith       ┆ 28  │
# │ Bob        ┆ Smith       ┆ 30  │
# │ Alice      ┆ Jones       ┆ 18  │
# └────────────┴─────────────┴─────┘
```

## `unique`

Keep the first row of each unique record. This is equivalent to `distinct` with all columns.

```python
from tabeline import DataFrame

df = DataFrame(
    given_name=["Alice", "Bob", "Alice", "Alice", "Bob"],
    family_name=["Smith", "Smith", "Smith", "Jones", "Smith"],
    age=[28, 30, 30, 18, 30],
)

df.unique()
# shape: (4, 3)
# ┌────────────┬─────────────┬─────┐
# │ given_name ┆ family_name ┆ age │
# │ ---        ┆ ---         ┆ --- │
# │ str        ┆ str         ┆ i64 │
# ╞════════════╪═════════════╪═════╡
# │ Alice      ┆ Smith       ┆ 28  │
# │ Bob        ┆ Smith       ┆ 30  │
# │ Alice      ┆ Smith       ┆ 30  │
# │ Alice      ┆ Jones       ┆ 18  │
# └────────────┴─────────────┴─────┘
```
