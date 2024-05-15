---
icon: material/table-of-contents
---

# Overview

This is an index of the main functionality available in Tabeline. Each constructor and verb has a link to more detailed documentation. The expression functions do not yet have detailed documentation, but should be self-explanatory.

## Creation

These are the ways to create a `DataFrame` from something that is not already a `DataFrame`

* [`DataFrame(**columns)`](creation.md#dataframe): Construct data frame directly from columns
* [`DataFrame.from_dict(columns)`](creation.md#dataframefrom_dict): Construct data frame directly from columns
* [`DataFrame.read_csv(filename)`](creation.md#dataframeread_csv): Read data frame from CSV file
* [`DataFrame.from_pandas(df)`](creation.md#dataframefrom_pandas): Convert from Pandas `DataFrame`
* [`DataFrame.from_polars(df)`](creation.md#dataframefrom_polars): Convert from Polars `DataFrame`

## Export

These are the various things that a `DataFrame` can be converted into

* [`to_dict()`](export.md#to_dict): Convert to dictionary of columns
* [`to_pandas()`](export.md#to_pandas): Convert to Pandas `DataFrame`
* [`to_polars()`](export.md#to_polars): Convert to Polars `DataFrame`
* [`write_csv(filename)`](export.md#to_csv): Write to CSV file

## Verbs

Each verb is a method of `DataFrame`.

### Column reorganization

* [`select`](verbs/select.md#select): Keep given columns
* [`deselect`](verbs/select.md#deselect): Drop given columns
* [`rename`](verbs/select.md#rename): Rename columns

### Row removal

* [`filter`](verbs/filter.md#filter): Keep rows for which predicate is true
* [`slice0`](verbs/filter.md#slice0): Keep rows given by 0-index
* [`slice1`](verbs/filter.md#slice1): Keep rows given by 1-index
* [`distinct`](verbs/filter.md#distinct): Drop rows with duplicate values under given columns
* [`unique`](verbs/filter.md#unique): Drop rows with duplicate values under all columns

### Row reordering

* [`sort`](verbs/sort.md#sort): Sort data frame according to given columns
* [`cluster`](verbs/sort.md#cluster): Bring rows together with same values under given columns

### Column mutation

* [`mutate`](verbs/mutate.md#mutate): Create or update columns according to given expressions
* [`transmute`](verbs/mutate.md#transmute): Mutate while dropping existing columns

### Grouping

* [`group_by`](verbs/group_by.md#group_by): Create a group level containing given columns
* [`ungroup`](verbs/group_by.md#ungroup): Drop the last group level

### Summarizing

* [`summarize`](verbs/summarize.md#summarize): Reduce each group to a single row according to given expressions

### Reshaping

* [`spread`](verbs/spread.md#spread): Reshape from long format to wide format
* [`gather`](verbs/spread.md#gather): Reshape from wide format to long format

### Joining

* [`inner_join`](verbs/join.md#inner_join): Merge data frames, dropping unmatched
* [`outer_join`](verbs/join.md#outer_join): Merge data frames, adding nulls for unmatched
* [`left_join`](verbs/join.md#left_join): Merge data frames, adding nulls for unmatched on the left data frame

### Concatenating

* [`concatenate_rows`](verbs/concatenate.md#concatenate_rows): Concatenate rows of data frames
* [`concatenate_columns`](verbs/concatenate.md#concatenate_columns): Concatenate columns of data frames

## Functions

These are the operators and functions available in the string expressions.

### Operators

If either operand is null, the result is null.

* `x + y`: `x` plus `y` or, if strings, `x` concatenated to `y`
* `x - y`: `x` minus `y`
* `x * y`: `x` times `y`
* `x / y`: `x` divided by `y`
* `x % y`: `x` mod `y`
* `x ** y`: `x` to the power of `y`

### Numeric to numeric broadcast

The functions in this section mathematical operations on numbers. If these functions receive scalar inputs, they return a scalar. If they receive any array inputs, any scalars are interpreted as constant vectors and an array is returned. For each null element, the result is null.

* `abs(x)`: Absolute value of `x`
* `sqrt(x)`: Square root of `x`
* `log(x)`: Natural logarithm of `x`
* `log2(x)`: Base-2 logarithm of `x`
* `log10(x)`: Base-10 logarithm of `x`
* `exp(x)`: Euler's number `e` to the power of `x`
* `pow(x, y)`: `x` to the power of `y`
* `sin(x)`: Sine of `x`
* `cos(x)`: Cosine of `x`
* `tan(x)`: Tangent of `x`
* `arcsin(x)`: Inverse sine of `x`
* `arccos(x)`: Inverse cosine of `x`
* `arctan(x)`: Inverse tangent of `x`
* `floor(x)`: `x` rounded down to the nearest integer
* `ceil(x)`: `x` rounded up to the nearest integer

### Numeric to boolean broadcast

For each null element, the result is null.

* `is_nan(x)`: True if `x` value is a floating point `NaN`
* `is_finite(x)`: True if `x` value is a floating point finite number

### Casting broadcast

The functions in this section convert values from one type to another. These are completely dependent on the behavior of the Polars [`cast`](https://pola-rs.github.io/polars/py-polars/html/reference/expressions/api/polars.Expr.cast.html) function. Nulls are preserved.

* `to_boolean(x)`: Convert `x` from a boolean, a float, or an integer, to a boolean
* `to_integer(x)`: Convert `x` from a boolean, a float, or an integer to an integer or parse a string as an integer
* `to_float(x)`: Convert `x` from a boolean, a float, or an integer to a float or parse a string as a float
* `to_string(x)`: Deparse `x` to a string

### Other broadcast

* `is_null(x)`: True if `x` is null. This is one of the few functions that returns a non-null value on null inputs.
* `if_else(condition, true_value, false_value)`: If `condition` is true, return `true_value`, otherwise return `false_value`.

### Numeric to numeric reduction

The functions in this section consume an entire column of numbers and to produce a scalar number. If any element is null, the result is null.

* `std(x)`: Population standard deviation of `x`
* `var(x)`: Population variance of `x`
* `max(x)`: Maximum of `x`
* `min(x)`: Minimum of `x`
* `sum(x)`: Sum of `x`
* `mean(x)`: Mean of `x`
* `median(x)`: Median of `x`
* `quantile(x, quantile)`: The `quantile` of `x` obtained via linear interpolation
  * `quantile` must be a `float` literal not an expression
* `trapz(x, y)`: Numerically integrate `y` over `x` using the trapezoidal rule
* `interp(x, xp, fp)`: Linearly interpolate `fp` over `xp` at `x`; typically, `x` is a float literal

### Boolean to boolean reduction

The functions in this section consume an entire column of booleans and to produce a scalar boolean. These follow [Kleene logic](https://en.wikipedia.org/wiki/Three-valued_logic#Kleene_and_Priest_logics) with respect to null.

* `any(x)`: True if any of `x` are true
* `all(x)`: True is all of `x` are true

### Any to any reduction

The functions in this section consume an entire column of anything and to produce a scalar of that type. These treat nulls as normal values.

* `first(x)`: The first value of `x`
* `last(x)`: The last value of `x`
* `same(x)`: One value of `x` if all values of `x` are the same, otherwise error

### Argumentless functions

The functions in this section evalute in the context of the `DataFrame`, not any particular column.

* `n()`: The number of rows in the `DataFrame`
* `row_index0()`: The 0-index of each row
* `row_index1()`: The 1-index of each row
