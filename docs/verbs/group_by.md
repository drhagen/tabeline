---
icon: material/format-list-group
---

# Changing group levels

`group_by` is not so much a verb as it is a preposition. `group_by` does not change the contents or orders of any rows or columns, but it changes the context of subsequent verbs. All rows which have the same values in all `group_by` columns are members of the same subframe. Subsequent verbs act as if they are applied each subframe individually. So in `filter` or `mutate`, an expression containing `max` or `mean` will apply only to the rows in each subframe.

Tabeline is different from all popular data grammar libraries in how it handles groups. An instance of `DataFrame` has group levels. Each invocation of `group_by` adds one group level, which can contain any number of columns names by which to group. The flattened list of group names from all levels can be accessed via the `group_names` property.

## `group_by`

Add a set of column names as a new group level. The column names must exist, and they must not be previously grouped.

```python
from tabeline import DataFrame

df = DataFrame(
    id=["a", "a", "b", "b"],
    x=[1, 2, 3, 4],
)

df.group_by("id").mutate(mean="mean(x)")
# group levels: [id]
# shape: (4, 3)
# ┌─────┬─────┬──────┐
# │ id  ┆ x   ┆ mean │
# │ --- ┆ --- ┆ ---  │
# │ str ┆ i64 ┆ f64  │
# ╞═════╪═════╪══════╡
# │ a   ┆ 1   ┆ 1.5  │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ a   ┆ 2   ┆ 1.5  │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ b   ┆ 3   ┆ 3.5  │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ b   ┆ 4   ┆ 3.5  │
# └─────┴─────┴──────┘
```

## `ungroup`

Drop the last group level.

The existence of group levels causes this to behave differently from dplyr. This does not remove all group names, only those present in the last group level.

```python
from tabeline import DataFrame

df = DataFrame(
    id=["a", "a", "b", "b"],
    x=[1, 2, 3, 4],
)

df.group_by("id").mutate(mean="mean(x)")
# shape: (4, 3)
# ┌─────┬─────┬──────┐
# │ id  ┆ x   ┆ mean │
# │ --- ┆ --- ┆ ---  │
# │ str ┆ i64 ┆ f64  │
# ╞═════╪═════╪══════╡
# │ a   ┆ 1   ┆ 2.5  │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ a   ┆ 2   ┆ 2.5  │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ b   ┆ 3   ┆ 2.5  │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ b   ┆ 4   ┆ 2.5  │
# └─────┴─────┴──────┘
```
