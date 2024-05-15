---
icon: material/swap-vertical
---

# Row reordering

The `sort` and `cluster` verbs change the order of rows. The individual rows are unchanged.

## `sort`

Sort rows according to the given column names. The data frame is sorted by the first column name using subsequent columns to break any ties.

```python
from tabeline import DataFrame

df = DataFrame(
    patient_id=[2, 1, 2, 1, 2, 1],
    t=[0.0, 0.0, 6.0, 6.0, 24.0, 24.0],
    measurement=[6.0, 5.5, 4.2, 4.0, 3.1, 3.0],
)

df.sort("patient_id", "t")
# ┌────────────┬──────┬─────────────┐
# │ patient_id ┆ t    ┆ measurement │
# │ ---        ┆ ---  ┆ ---         │
# │ i64        ┆ f64  ┆ f64         │
# ╞════════════╪══════╪═════════════╡
# │ 1          ┆ 0.0  ┆ 5.5         │
# ├╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 1          ┆ 6.0  ┆ 4.0         │
# ├╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 1          ┆ 24.0 ┆ 3.0         │
# ├╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 2          ┆ 0.0  ┆ 6.0         │
# ├╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 2          ┆ 6.0  ┆ 4.2         │
# ├╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 2          ┆ 24.0 ┆ 3.1         │
# └────────────┴──────┴─────────────┘
```


## `cluster`

Bring together all the rows with the same value under the given columns. A side effect of `sort` is that all rows with the same key value under some given columns are brought together. If you want this clustering, without the sorting, `cluster` will bring all the rows with a given key together, but retain the order of first instance of that key.

```python
from tabeline import DataFrame

df = DataFrame(
    patient_id=[2, 1, 2, 1, 2, 1],
    t=[0.0, 0.0, 6.0, 6.0, 24.0, 24.0],
    measurement=[6.0, 5.5, 4.2, 4.0, 3.1, 3.0],
)

df.cluster("patient_id")
shape: (6, 3)
# ┌────────────┬──────┬─────────────┐
# │ patient_id ┆ t    ┆ measurement │
# │ ---        ┆ ---  ┆ ---         │
# │ i64        ┆ f64  ┆ f64         │
# ╞════════════╪══════╪═════════════╡
# │ 2          ┆ 0.0  ┆ 6.0         │
# ├╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 2          ┆ 6.0  ┆ 4.2         │
# ├╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 2          ┆ 24.0 ┆ 3.1         │
# ├╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 1          ┆ 0.0  ┆ 5.5         │
# ├╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 1          ┆ 6.0  ┆ 4.0         │
# ├╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ 1          ┆ 24.0 ┆ 3.0         │
# └────────────┴──────┴─────────────┘
```
