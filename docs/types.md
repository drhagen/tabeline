---
icon: material/graph-outline
---

# Types

Tabeline has a well-defined type system, exposing a subset of the data types available in Arrow.
Each column has a data type determining the set of possible values that column can hold.

Some verbs evaluate expressions of column names, specifically `filter`, `mutate`, `transmute`, and `summarize`.
Before evaluation, the expressions are statically type checked in the context of the data frame types.

## Data types

The data types are defined as members of the enum `tabeline.DataType`.

| Type | Description |
|------|-------------|
| `Boolean` | true or false |
| `Whole8` | 0 to 255 |
| `Whole16` | 0 to 2^16-1 |
| `Whole32` | 0 to 2^32-1 |
| `Whole64` | 0 to 2^64-1* |
| `Integer8` | -128 to 127 |
| `Integer16` | -2^15 to 2^15-1 |
| `Integer32` | -2^31 to 2^31-1 |
| `Integer64` | -2^63 to 2^63-1* |
| `Float32` | 32-bit IEEE 754 floating point |
| `Float64` | 64-bit IEEE 754 floating point |
| `String` | Unicode string |
| `Nothing` | The bottom type |

*Limitations in how PyO3 communicates between Rust and Python may create edge cases for whole numbers and integers whose absolute value is larger then 2^63-1.

## Expression types

The expression types are defined as members of the private enum `ExpressionType`.
It is private because all expressions are provided to Tabeline as strings.
There is currently no access in Python to the expresion evaluation engine written in Rust.
Nevertheless, these types are useful for understanding how static type checking of expression is done.

Each column of a data frame is an `Array[Element <: DataType]`.
For example, a column of type `Array[Integer8]` contains only 8-bit integers or nulls.
In Tabeline, there is no way to represent an array with no nulls—any column may have nulls.
A column with only nulls is represented by `Array[Nothing]`, which appears most often as the inferred type of an empty array.

Most operations broadcast along the arrays, so expressions of arrays are often arrays themselves.
For example, in a dataframe `DataFrame(a=[1,2,3], b=[4,5,6])`, `a`, `b`, and `a+b` will all have type `Array[Integer64]`.

Reduction functions, such as `max` or `first`, turn an array into a scalar.
A scalar is represented in the type system as `Scalar[Element <: DataType]`.
Some verbs, such as `summarize` require that their expressions evaluate to a scalar.
This is validated via static type checking of the expression.

## Casting

Tabeline employs a thoughtful approach to converting numeric types when the given types are not appropriate for the problem.
There are some overarching principles that are applied consistently among all operations.

Unlike other libraries, Tabeline does not cast from boolean to numeric or from numeric to boolean.
Use the `to_boolean`, `to_integer`, and `to_float` functions to manually convert between these types.

Also, Tabeline does not cast freely to strings. Use `to_string` to get a string representation of any type.

### Consistency

Operations that accept multiple numeric arguments can typically only be applied to arguments of the same type.
The one exception is exponentiation and the `pow` function.
Arguments of different numeric types are cast to the most complex type using the following algorithm.

1. If any of the arguments are floats, all are cast to floats.
    1. If any are `Float64`, all are cast to `Float64`.
    2. Otherwise, cast to `Float32`.
2. Else if any of the arguments are integers, all are cast to integers of the largest width.
    - Not only is the widest integer considered, but the widest whole type also.
3. Otherwise, they are only whole numbers and are cast to the largest width.

### Signed operations

Some operations that are not closed on the whole numbers—for example, negation and subtraction.
In such cases, wholes are cast to integers.

### Float operations

Some operations are not closed on the integers—for example, division and trancendental functions.
In such cases, wholes and integers are cast to floats using the following algorithm.

1. If any arguments are `Float64`, all are cast to `Float64`.
2. Else if any are `Float32`, all are cast to `Float32`.
3. Otherwise, they are only whole numbers and integers, which are cast to `Float64`.

### Literals

Numeric literals are numbers written in the expression itself (e.g. `2` or `-3` or `3.5`).
Literals belong to a particular category (whole, integer, or float), but they don't have a well-defined size.
A non-negative integer literal will act like the smallest whole type that will fit the number.
A negative integer literal will act like the smallest integer type that will fit the number.
A decimal literal will act like a float of no particular size.
Operations involving a literal will cause the literal to be cast to a concrete type.
If they are not cast to a particular type by being involved in an operation with a concrete type, they will default to the 64-bit size of their respective category.

```python
from tabeline import Array, DataFrame, DataType

df = DataFrame(
    x=Array[DataType.Whole8](0, 1, 2),
)

df.transmute(x_plus_1="x + 1", x_minus_1="x - 1", x_plus_1000="x + 1000")
# shape: (3, 3)
# ┌──────────┬───────────┬─────────────┐
# │ x_plus_1 ┆ x_minus_1 ┆ x_plus_1000 │
# │ ---      ┆ ---       ┆ ---         │
# │ u8       ┆ i8        ┆ u16         │
# ╞══════════╪═══════════╪═════════════╡
# │ 1        ┆ -1        ┆ 1000        │
# │ 2        ┆ 0         ┆ 1001        │
# │ 3        ┆ 1         ┆ 1002        │
# └──────────┴───────────┴─────────────┘
```
