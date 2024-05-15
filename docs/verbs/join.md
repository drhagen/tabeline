---
icon: material/set-center
---

# Joining two data frames

The `inner_join`, `outer_join`,  and `left_join` verbs perform the classic table join operations.

# `inner_join`

This method performs the classic inner join operation. Rows on either side that are missing a corresponding row on the other side are dropped. Rows on either side that have multiple matches on the other side are duplicated.

```python
from tabeline import DataFrame

df1 = DataFrame(x=[0, 1, 2, 3, 4], y=["a", "b", "c", "d", "e"])
df2 = DataFrame(x=[3, 2, -1, 1, 0], z=["a", "b", "z", "c", "d"])

df1.inner_join(df2)
# shape: (4, 3)
# ┌─────┬─────┬─────┐
# │ x   ┆ y   ┆ z   │
# │ --- ┆ --- ┆ --- │
# │ i64 ┆ str ┆ str │
# ╞═════╪═════╪═════╡
# │ 0   ┆ a   ┆ d   │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
# │ 1   ┆ b   ┆ c   │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
# │ 2   ┆ c   ┆ b   │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
# │ 3   ┆ d   ┆ a   │
# └─────┴─────┴─────┘
```

# `outer_join`

This method performs the classic outer join (or full join) operation. Rows on either side that are missing a corresponding row on the other side are kept, filling the other side with nulls. Rows on either side that have multiple matches on the other side are duplicated.

```python
from tabeline import DataFrame

df1 = DataFrame(x=[0, 1, 2, 3, 4], y=["a", "b", "c", "d", "e"])
df2 = DataFrame(x=[3, 2, -1, 1, 0], z=["a", "b", "z", "c", "d"])

df1.outer_join(df2)
# shape: (6, 3)
# ┌─────┬──────┬──────┐
# │ x   ┆ y    ┆ z    │
# │ --- ┆ ---  ┆ ---  │
# │ i64 ┆ str  ┆ str  │
# ╞═════╪══════╪══════╡
# │ -1  ┆ null ┆ z    │
# ├╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ 0   ┆ a    ┆ d    │
# ├╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ 1   ┆ b    ┆ c    │
# ├╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ 2   ┆ c    ┆ b    │
# ├╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ 3   ┆ d    ┆ a    │
# ├╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ 4   ┆ e    ┆ null │
# └─────┴──────┴──────┘
```

# `left_join`

This method performs the classic left join operation. Rows on the left side that are missing a corresponding row on the right side are kept, filling the right side with nulls. Rows on the right side that are missing a corresponding row on the left side are dropped. Rows on either side that have multiple matches on the other side are duplicated.

```python
from tabeline import DataFrame

df1 = DataFrame(x=[0, 1, 2, 3, 4], y=["a", "b", "c", "d", "e"])
df2 = DataFrame(x=[3, 2, -1, 1, 0], z=["a", "b", "z", "c", "d"])

df1.left_join(df2)
# shape: (5, 3)
# ┌─────┬─────┬──────┐
# │ x   ┆ y   ┆ z    │
# │ --- ┆ --- ┆ ---  │
# │ i64 ┆ str ┆ str  │
# ╞═════╪═════╪══════╡
# │ 0   ┆ a   ┆ d    │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ 1   ┆ b   ┆ c    │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ 2   ┆ c   ┆ b    │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ 3   ┆ d   ┆ a    │
# ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ 4   ┆ e   ┆ null │
# └─────┴─────┴──────┘
```
