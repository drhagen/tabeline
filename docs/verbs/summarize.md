---
icon: material/arrow-collapse-all
---

# Reducing subframes

## `summarize`

Reduce each subframe to a single row. This operation can only be applied to a data frame with at least one group level. The result has one column for each group column name and one column for each named argument. The name of the argument becomes the column name and the value of the argument must be an expression that evaluates to a scalar. That scalar will be the value of the cell for each summarized subframe. The last group level is dropped.

```python
from tabeline import DataFrame

df = DataFrame(
    id=["a", "a", "b", "b"],
    x=[1, 2, 3, 4],
)

df.group_by("id").summarize(x="mean(x)")
# shape: (2, 2)
# ┌─────┬─────┐
# │ id  ┆ x   │
# │ --- ┆ --- │
# │ str ┆ f64 │
# ╞═════╪═════╡
# │ a   ┆ 1.5 │
# ├╌╌╌╌╌┼╌╌╌╌╌┤
# │ b   ┆ 3.5 │
# └─────┴─────┘
```