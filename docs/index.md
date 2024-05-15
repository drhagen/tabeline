---
icon: material/home
---

# Tabeline

Tabeline is a data frame and data grammar library. You write the expressions in strings and supply them to methods on the `DataFrame` class, like `df.filter("t <= 24")`. The  strings are parsed by Parsita and converted into Polars for execution.

Tabeline draws inspiration from [dplyr](https://dplyr.tidyverse.org/), the data grammar of R's tidyverse. The `filter`, `mutate`, `group_by`, and `summarize` methods should all feel familiar. But Tabeline is as proper a Python library as can be, using methods instead of pipe operators.

Tabeline uses Polars under the hood, but adds a lot of handling of edge cases from Polars, which otherwise result in crashes or behavior that is not type stable.

## Installation

It is recommended to install Tabeline from PyPI using `pip`.

```shell
pip install tabeline
```

## Motivating example

```python
from tabeline import DataFrame

# Construct a data frame using clean syntax
# from_csv, from_pandas, and from_polars are also available
df = DataFrame(
    id=[0, 0, 0, 0, 1, 1, 1, 1, 1],
    t=[0, 6, 12, 24, 0, 6, 12, 24, 48],
    y=[0, 2, 3, 1, 0, 4, 3, 2, 1],
)

# Use data grammar methods and string expressions to define
# transformed data frames
analysis = (
    df
    .filter("t <= 24")
    .group_by("id")
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

## Data grammar

A data grammar is a particular style of data frame library popularized by Hadley Wickham via the [dplyr](https://dplyr.tidyverse.org/) package in R. In a library written as a data grammar, the data frame object has a relatively small number of methods. The parameters of most of these methods are columns names or expressions of column names. The return value of most of these methods is a new data frame. These methods that transform a data frame into another data frame by taking simple inputs are called the "verbs" of the data grammar. Each verb does a single simple transformation. By always returning a new data frame, the verbs can be cleanly combined via method chaining. The `filter` and `summarize` methods in the above example are two such verbs.

Users who want to do an analysis of a data frame, however basic, are unlikely to find a single function that does exactly what they want. This is by design. It is not feasible to make a data frame library that has a function for every kind of analysis someone would want. Tabeline expects users to learn the data grammar so that they can split the analysis into steps than can be performed by verbs.

### Expressions

Tabeline uses strings to encapsulate expressions. The `"t <= 24"` and `"trapz(t, y)"` strings in above example are two such expressions. These strings are parsed and executed. The reason for using strings is that there is no cleaner way to write expressions in Python that need to be evaluated in a different context, namely in the context of the data frame.

In R, all functions are effectively macros that can capture any expressions they are given to be executed at a later time. For example, `df %>% filter(t <= 24)` in dplyr evaluates using the `t` column in the data frame, not the `t` variable in the outer scope, if it is even defined.

In Python, the closest thing is the `lambda`. It would be trivial to make an interface that took a single argument function, which would be passed the data frame or some modified version of the data frame. For example, `df.filter(lambda df: df.t <= 24)`. However, anonymous functions have particularly bad syntax in Python, and they work particularly badly in the face of multiple arguments (like would be needed for `mutate`). The `lambda` operator has lower precedence than the commas that separate arguments, so most lambdas need to be surrounded by parentheses.
