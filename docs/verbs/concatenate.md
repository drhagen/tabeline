---
icon: material/table-multiple
---

# Concatenating multiple data frames

The `concatenate_rows` and `concatenate_columns` functions are not really verbs in the data grammar, but are more like conjunctions. They are the only operations that take an arbitrary number of data frames as arguments. As such, they are genuine Python functions importable from `tabeline`, not methods of `DataFrame`.

## `concatenate_rows`

Concatenate the rows of the given data frames into a single data frame. The data frames must have the same columns, in the same order. Typically, only data frames without grouping are concatenated, but concatenation will be allowed if all group levels are identical. In other libraries, this operation may be called "row binding" or "vertical stacking".

```python
from tabeline import DataFrame, concatenate_rows

study1 = DataFrame(study=[1, 1, 1], subject=[10, 11, 12])
study2 = DataFrame(study=[2, 2, 2], subject=[20, 21, 22])

concatenate_rows(study1, study2)
# shape: (6, 2)
# ┌───────┬─────────┐
# │ study ┆ subject │
# │ ---   ┆ ---     │
# │ i64   ┆ i64     │
# ╞═══════╪═════════╡
# │ 1     ┆ 10      │
# │ 1     ┆ 11      │
# │ 1     ┆ 12      │
# │ 2     ┆ 20      │
# │ 2     ┆ 21      │
# │ 2     ┆ 22      │
# └───────┴─────────┘
```

## `concatenate_columns`

Concatenate the columns of the given data frames into a single data frame. All data frames must have the same number of rows. No columns may be duplicated. No group levels may be present. In other libraries, this operation may be called "column binding" or "horizontal stacking".

This is one of the most dangerous operations in Tabeline. Often, [`inner_join`](../verbs/join.md#inner_join) is a safer choice than `concatenate_columns`. Joining on key columns ensures that the data is correctly matched even if the row order is mixed up.

```python
from tabeline import DataFrame, concatenate_columns

study1 = DataFrame(study=[1, 1, 1], subject=[10, 10, 11])
study2 = DataFrame(measurements=[12.5, 12.0, 5.6])

concatenate_columns(study1, study2)
# shape: (3, 3)
# ┌───────┬─────────┬──────────────┐
# │ study ┆ subject ┆ measurements │
# │ ---   ┆ ---     ┆ ---          │
# │ i64   ┆ i64     ┆ f64          │
# ╞═══════╪═════════╪══════════════╡
# │ 1     ┆ 10      ┆ 12.5         │
# │ 1     ┆ 10      ┆ 12.0         │
# │ 1     ┆ 11      ┆ 5.6          │
# └───────┴─────────┴──────────────┘
```
