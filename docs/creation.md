---
icon: material/tree
---

# Creating a data frame

The central class of Tabeline is `tabeline.DataFrame`. There is little to do with Tabeline other than constructing a `DataFrame` and invoking methods on it to get a different `DataFrame`.

To create a `DataFrame`, you can either use the constructor or several static methods on the class.


## `DataFrame`

The constructor for `DataFrame` takes an arbitrary number of named arguments. The name of each argument creates a column with the same name. The value of each named argument must be a list, which becomes the values under that column. Naturally, all provided lists must have the same length.

```python
from tabeline import DataFrame

df = DataFrame(
    name=["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    episode=[4, 5, 6],
    release_year=[1977, 1980, 1983],
)
```

!!! note

    If you poke around in the code, you may notice that the contructor also takes positional arguments. Those are part of the private constructor; don't use them.


## `DataFrame.from_dict`

This is basically the same as the constructor, except the arguments are kept as a single dictionary instead of being splatted out. The values of the dictionary can be any `Sequence`.

```python
from tabeline import DataFrame

data = {
    "name": ["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    "episode": [4, 5, 6],
    "release_year": [1977, 1980, 1983],
}

df = DataFrame.from_dict(data)
```

See also [`DataFrame.to_dict`](export.md#to_dict).


## `DataFrame.read_csv`

Reads a data frame from a CSV file.

```python
from pathlib import Path
from tabeline import DataFrame

df = DataFrame.read_csv(Path("star_wars.csv"))
```

See also [`DataFrame.write_csv`](export.md#write_csvfilename).


## `DataFrame.from_pandas`

Create a `tabeline.DataFrame` from a `pandas.DataFrame`. This ignores the index. Use `df.reset_index()` on the Pandas `DataFrame` to copy the index to columns first. This requires that the `pandas` extra is installed (i.e. `pip install tabeline[pandas]`) because this conversion through Polars relies on PyArrow, which may not otherwise be installed.

```python
import pandas as pd
from tabeline import DataFrame

pandas_df = pd.DataFrame(dict(
    name=["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    episode=[4, 5, 6],
    release_year=[1977, 1980, 1983],
))

df = DataFrame.from_pandas(pandas_df)
```

See also [`DataFrame.to_pandas`](export.md#to_pandas).


## `DataFrame.from_polars`

Create a `tabeline.DataFrame` from a `polars.DataFrame`. Because Tabeline uses Polars internally, this is a simple wrapper.

```python
import polars as pl
from tabeline import DataFrame

polars_df = pl.DataFrame(dict(
    name=["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    episode=[4, 5, 6],
    release_year=[1977, 1980, 1983],
))

df = DataFrame.from_polars(polars_df)
```

See also [`DataFrame.to_polars`](export.md#to_polars).
