---
icon: material/table-pivot
---

# Pivoting between wide and tall formats

The `spread` and `gather` verbs reshape a data frame between long format and wide format of data representation.

## `spread`

Turn a long data frame into a wide data frame. This operation takes the names of two columns, a key column and a value column. Every value in the key column becomes a column name and every value in the value column becomes a value under its respective column.

`spread` is a reduction verb. As such, it drops the last group level, and it cannot be applied to data frames with no group levels.

```python
from tabeline import DataFrame

df = DataFrame(
    grades=[0, 0, 1, 1, 2, 2],
    sex=["M", "F", "M", "F", "M", "F"],
    count=[8, 9, 9, 10, 6, 9],
)

df.group_by("sex").spread("grades", "count")
# shape: (2, 4)
# ┌─────┬─────┬─────┬─────┐
# │ sex ┆ 0   ┆ 1   ┆ 2   │
# │ --- ┆ --- ┆ --- ┆ --- │
# │ str ┆ i64 ┆ i64 ┆ i64 │
# ╞═════╪═════╪═════╪═════╡
# │ M   ┆ 8   ┆ 9   ┆ 6   │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
# │ F   ┆ 9   ┆ 10  ┆ 9   │
# └─────┴─────┴─────┴─────┘
```

## `gather`

Turn a wide data frame into a long data frame. This operation takes the name of a key column that not exist, the name of a value column that does not exist, and an arbitrary number of existing column names. Each value under the existing columns is converted to a value under the new value column, with the name of the column put next to it under the key column.

`gather` adds one group level containing the key column name.

```python
from tabeline import DataFrame

df = DataFrame.from_dict({
    "sex": ["M", "F"],
    "0": [8, 9],
    "1": [9, 10],
    "2": [6, 9]},
)

df.gather("grades", "count", "0", "1", "2")
# group levels: [grades]
# shape: (6, 3)
# ┌─────┬────────┬───────┐
# │ sex ┆ grades ┆ count │
# │ --- ┆ ---    ┆ ---   │
# │ str ┆ str    ┆ i64   │
# ╞═════╪════════╪═══════╡
# │ M   ┆ 0      ┆ 8     │
# ├╌╌╌╌╌┼╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┤
# │ F   ┆ 0      ┆ 9     │
# ├╌╌╌╌╌┼╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┤
# │ M   ┆ 1      ┆ 9     │
# ├╌╌╌╌╌┼╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┤
# │ F   ┆ 1      ┆ 10    │
# ├╌╌╌╌╌┼╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┤
# │ M   ┆ 2      ┆ 6     │
# ├╌╌╌╌╌┼╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┤
# │ F   ┆ 2      ┆ 9     │
# └─────┴────────┴───────┘
```
