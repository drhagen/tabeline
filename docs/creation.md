# Creating a table

The central class of Tabeline is `tabeline.DataTable`. There is little to do with Tabeline other than constructing a `DataTable` and invoking methods on it to get a different `DataTable`.

To create a `DataTable`, you can either use the constructor or several static methods on the class.


## `DataTable`

The constructor for `DataTable` takes an arbitrary number of named arguments. The name of each argument creates a column with the same name. The value of each named argument must be a list, which becomes the values under that column. Naturally, all provided lists must have the same length.

```python
from tabeline import DataTable

table = DataTable(
    name=["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    episode=[4, 5, 6],
    release_year=[1977, 1980, 1983],
)
```

!!! note

    If you poke around in the code, you may notice that the contructor also takes positional arguments. Those are part of the private constructor; don't use them.


## `DataTable.read_csv`

Reads a table from a CSV file.

```python
from pathlib import Path
from tabeline import DataTable

table = DataTable.read_csv(Path("star_wars.csv"))
```


## `DataTable.from_pandas`

Create a `tabeline.DataTable` from a `pandas.DataFrame`. This ignores the index. Use `df.reset_index()` on the Pandas `DataFrame` to copy the index to columns first.

```python
from polars import DataFrame
from tabeline import DataTable

df = DataFrame(dict(
    name=["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    episode=[4, 5, 6],
    release_year=[1977, 1980, 1983],
))

table = DataTable.from_pandas(df)
```


## `DataTable.from_polars`

Create a `tabeline.DataTable` from a `polars.DataFrame`. Because Tabeline uses Polars internally, this is a simple wrapper.

```python
from polars import DataFrame
from tabeline import DataTable

df = DataFrame(dict(
    name=["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
    episode=[4, 5, 6],
    release_year=[1977, 1980, 1983],
))

table = DataTable.from_polars(df)
```
