# Index

This is an index of the main functionality available in Tabeline. Each constructor and verb has a link to more detailed documentation. The expression functions do not yet have detailed documentation, but should be self-explanatory.

## Creation

These are the ways to create a `DataTable` from something that is not already a `DataTable`

* [`DataTable(**columns)`](creation.md#datatable): Construct table directly from columns
* [`DataTable.read_csv(filename)`](creation.md#datatableread_csv): Read table from CSV file
* [`DataTable.from_pandas(df)`](creation.md#datatablefrom_pandas): Convert from Pandas `DataFrame`
* [`DataTable.from_polars(df)`](creation.md#datatablefrom_polars): Convert from Polars `DataFrame`

## Verbs

Each verb is a method of `DataTable`.

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

* [`sort`](verbs/sort.md#sort): Sort table according to given columns
* [`cluster`](verbs/sort.md#cluster): Bring rows together with same values under given columns

### Column mutation

* [`mutate`](verbs/mutate.md#mutate): Create or update columns according to given expressions
* [`transmute`](verbs/mutate.md#transmute): Mutate while dropping existing columns

### Grouping

* [`group`](verbs/group.md#group): Create a group level containing given columns
* [`ungroup`](verbs/group.md#ungroup): Drop the last group level

### Summarizing

* [`summarize`](verbs/summarize.md#summarize): Reduce each group to a single row according to given expressions

### Reshaping

* [`spread`](verbs/spread.md#spread): Reshape from long format to wide format
* [`gather`](verbs/spread.md#gather): Reshape from wide format to long format

### Joining

* [`inner_join`](verbs/join.md#inner_join): Merge tables, dropping unmatched
* [`outer_join`](verbs/join.md#outer_join): Merge tables, adding nulls for unmatched
* [`left_join`](verbs/join.md#left_join): Merge tables, adding nulls for unmatched on the left table

## Functions

These are the operators and functions available in the string expressions.

### Operators

* `x + y`: `x` plus `y` or, if strings, `x` concatenated to `y`
* `x - y`: `x` minus `y`
* `x * y`: `x` times `y`
* `x / y`: `x` divided by `y`
* `x % y`: `x` mod `y`
* `x ** y`: `x` to the power of `y`

### Numeric to numeric broadcast

The functions in this section mathematical operations on numbers. If these functions receive scalar inputs, they return a scalar. If they receive any array inputs, any scalars are interpreted as constant vectors and an array is returned.

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
* `floor(x)`: `x` rounded down to the nearest integer
* `ceil(x)`: `x` rounded up to the nearest integer

### Numeric to boolean broadcast

* `is_nan`: True if numeric value is a floating point `NaN`

### Numeric to numeric reduction

The functions in this section consume an entire column of numbers and to produce a scalar number.

* `std(x)`: Population standard deviation of `x`
* `var(x)`: Population variacne of `x`
* `max(x)`: Maximum of `x`
* `min(x)`: Minimum of `x`
* `sum(x)`: Sum of `x`
* `mean(x)`: Mean of `x`
* `median(x)`: Median of `x`
* `quantile(x, quantile)`: The `quantile` of `x` obtained via linear interpolation
  * `quantile` must be a `float` not an expression
* `trapz(x, y)`: Numerically integrate `y` over `x` using the trapezoidal rule

### Boolean to boolean reduction

The functions in this section consume an entire column of booleans and to produce a scalar boolean.

* `any(x)`: True if any of `x` are true
* `all(x)`: True is all of `x` are true

### Any to any reduction

The functions in this section consume an entire column of anything and to produce a scalar of that type.

* `first(x)`: The first value of `x`
* `last(x)`: The last value of `x`
