---
icon: material/table-column-plus-after
---

# Creating new columns

The `mutate` and `transmute` verbs create new columns based on expressions of existing columns. The number of rows is unchanged.


## `mutate`

Create new columns or redefine existing columns. This takes an arbitrary number of named arguments. The name of each argument is the name of a column. The value of the argument is an expression that provides a definition for that column. If the column name already exists, that column will be replaced by the evaluation of the new definition. If the column name does not already exist, the new column will be appended to the existing columns.

```python
from tabeline import DataFrame

df = DataFrame(
    name=["wide", "tall", "square"],
    width=[5, 2, 3],
    height=[1, 4, 3],
)

df.mutate(area="width * height")
# ┌────────┬───────┬────────┬──────┐
# │ name   ┆ width ┆ height ┆ area │
# │ ---    ┆ ---   ┆ ---    ┆ ---  │
# │ str    ┆ i64   ┆ i64    ┆ i64  │
# ╞════════╪═══════╪════════╪══════╡
# │ wide   ┆ 5     ┆ 1      ┆ 5    │
# ├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ tall   ┆ 2     ┆ 4      ┆ 8    │
# ├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ square ┆ 3     ┆ 3      ┆ 9    │
# └────────┴───────┴────────┴──────┘
```

# `transmute`

Just like mutate except the existing columns are not kept. This is identical to `mutate` followed by `select` on the newly defined columns.

```python
from tabeline import DataFrame

df = DataFrame(
    name=["wide", "tall", "square"],
    width=[5, 2, 3],
    height=[1, 4, 3],
)

df.transmute(name="name", area="width * height")
# shape: (3, 2)
# ┌────────┬──────┐
# │ name   ┆ area │
# │ ---    ┆ ---  │
# │ str    ┆ i64  │
# ╞════════╪══════╡
# │ wide   ┆ 5    │
# ├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ tall   ┆ 8    │
# ├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ square ┆ 9    │
# └────────┴──────┘
```
