---
icon: material/swap-horizontal
---

# Column dropping and reordering

The `select`, `deselect`, and `rename` verbs change which columns are present in the data frame, their order, and what names they have. The content of the columns is unchanged.

## `select`

Keep only the columns whose names are listed, in the order they are listed.

```python
from tabeline import DataFrame

df = DataFrame(
    study=[1, 2],
    location=["USA", "USA"],
    cost=[3254, 11843],
    success=[True, False],
)

df.select("study", "success", "cost")
# shape: (2, 3)
# ┌───────┬─────────┬───────┐
# │ study ┆ success ┆ cost  │
# │ ---   ┆ ---     ┆ ---   │
# │ i64   ┆ bool    ┆ i64   │
# ╞═══════╪═════════╪═══════╡
# │ 1     ┆ true    ┆ 3254  │
# ├╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┤
# │ 2     ┆ false   ┆ 11843 │
# └───────┴─────────┴───────┘
```

## `deselect`

Drop the columns whose names are listed.

```python
from tabeline import DataFrame

df = DataFrame(
    study=[1, 2],
    location=["USA", "USA"],
    cost=[3254, 11843],
    success=[True, False],
)

df.deselect("location")
# shape: (2, 3)
# ┌───────┬───────┬─────────┐
# │ study ┆ cost  ┆ success │
# │ ---   ┆ ---   ┆ ---     │
# │ i64   ┆ i64   ┆ bool    │
# ╞═══════╪═══════╪═════════╡
# │ 1     ┆ 3254  ┆ true    │
# ├╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌┤
# │ 2     ┆ 11843 ┆ false   │
# └───────┴───────┴─────────┘
```

## `rename`

Change the name of some columns, keeping their original order unchanged. This takes named arguments, where the key is the new name and the value is the old name. In this, Tabeline is like [dyplr rename](https://dplyr.tidyverse.org/reference/rename.html) rather than [Polars rename](https://pola-rs.github.io/polars/py-polars/html/reference/api/polars.DataFrame.rename.html), which flips the order of the new and old names.

The renaming happens simultaneously, allowing column names to be swapped.

```python
from tabeline import DataFrame

df = DataFrame(
    name=[1, 2],
    full_name=["Alice", "Bob"],
    age=[27, 55],
    authorized=[True, True],
)

df.rename(name="full_name", id="name")
# shape: (2, 4)
# ┌─────┬───────┬─────┬────────────┐
# │ id  ┆ name  ┆ age ┆ authorized │
# │ --- ┆ ---   ┆ --- ┆ ---        │
# │ i64 ┆ str   ┆ i64 ┆ bool       │
# ╞═════╪═══════╪═════╪════════════╡
# │ 1   ┆ Alice ┆ 27  ┆ true       │
# ├╌╌╌╌╌┼╌╌╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 2   ┆ Bob   ┆ 55  ┆ true       │
# └─────┴───────┴─────┴────────────┘
```
