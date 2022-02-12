# Tabeline

Tabeline is a data table and data grammar library. You write the expressions in strings and supply them to methods on the `DataTable` class. The  strings are parsed by Parsita and converted into Polars for execution.

Tabeline draws inspiration from dplyr, the data grammar of R's tidyverse, especially for its methods names. The `filter`, `mutate`, `group`, and `summarize` methods should all feel familiar. But Tabeline is as proper a Python library as can be, using methods instead of pipes, like is standard in R. 

Tabeline uses Polars under the hood, but adds a lot of handling of edge cases from Polars, which otherwise result in crashes or behavior that is not type stable.

See the [Documentation](htps://tabeline.drhagen.com) for the full user guide.

## Installation

It is recommended to install Tabeline from PyPI using `pip`.

```shell
pip install tabeline
```

## Motivating example

```python
from tabeline import DataTable

# Construct a table using clean syntax
# from_csv, from_pandas, and from_polars are also available 
table = DataTable(
    id=[0, 0, 0, 0, 1, 1, 1, 1, 1],
    t=[0, 6, 12, 24, 0, 6, 12, 24, 48],
    y=[0, 2, 3, 1, 0, 4, 3, 2, 1],
)

# Use data grammar methods and string expressions to define
# transformed data tables
analysis = (
    table
    .filter("t <= 24")
    .group("id")
    .summarize(auc="trapz(t, y)")
)

print(analysis)
# shape: (2, 2)
# ┌─────┬──────┐
# │ id  ┆ auc  │
# │ --- ┆ ---  │
# │ i64 ┆ f64  │
# ╞═════╪══════╡
# │ 0   ┆ 45.0 │
# ├╌╌╌╌╌┼╌╌╌╌╌╌┤
# │ 1   ┆ 63.0 │
# └─────┴──────┘
```
