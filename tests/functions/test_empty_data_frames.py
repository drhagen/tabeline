import pytest

from tabeline import DataFrame

zero_argument_functions = [
    "n",
    "row_index0",
    "row_index1",
]

one_argument_elementwise_functions = [
    "abs",
    "sqrt",
    "log",
    "log2",
    "log10",
    "exp",
    "sin",
    "cos",
    "tan",
    "arcsin",
    "arccos",
    "arctan",
    "floor",
    "ceil",
    "is_nan",
    "is_finite",
    "to_boolean",
    "to_integer",
    "to_float",
    "to_string",
]

one_argument_math_reduction_functions = [
    "std",
    "var",
    "max",
    "min",
    "sum",
    "mean",
    "median",
]

one_argument_functions = [
    *one_argument_elementwise_functions,
    "is_null",
    "first",
    "last",
    "any",
    "all",
    "same",
    *one_argument_math_reduction_functions,
]


@pytest.mark.parametrize("name", zero_argument_functions)
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame().group_by().group_by(),
        DataFrame(a=[]).group_by("a"),
        DataFrame(a=[], b=[]).group_by("a", "b"),
        DataFrame(a=[], b=[]).group_by("a").group_by("b"),
    ],
)
def test_zero_argument_functions_on_rowless_data_frame_with_mutate(name, df):
    actual = df.mutate(x=f"{name}()")
    expected = df.mutate(x="1")
    assert actual == expected


# # https://github.com/pola-rs/polars/issues/15257
@pytest.mark.skip(reason="Polars operators do not work on all null columns")
@pytest.mark.parametrize("name", zero_argument_functions)
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(),
        DataFrame().group_by(),
        DataFrame(a=[]),
        DataFrame(a=[]).group_by("a"),
        DataFrame(a=[], b=[]).group_by("a", "b"),
        DataFrame(a=[], b=[]).group_by("a").group_by("b"),
    ],
)
def test_zero_argument_functions_on_rowless_data_frame_with_summarize(name, df):
    actual = df.group_by().summarize(x=f"{name}()")
    expected = df.mutate(x="1")
    assert actual == expected


@pytest.mark.parametrize("name", one_argument_functions)
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(a=[]),
        DataFrame(a=[]).group_by(),
        DataFrame(a=[]).group_by().group_by(),
        DataFrame(a=[]).group_by("a"),
        DataFrame(a=[], b=[], c=[]).group_by("a", "b"),
        DataFrame(a=[], b=[], c=[]).group_by("a").group_by("b"),
    ],
)
def test_one_argument_functions_on_rowless_data_frame_with_mutate(name, df):
    actual = df.mutate(x=f"{name}(a)")
    expected = df.mutate(x="a")
    assert actual == expected


# https://github.com/pola-rs/polars/issues/15257
@pytest.mark.skip(reason="Polars operators do not work on all null columns")
@pytest.mark.parametrize("name", one_argument_functions)
@pytest.mark.parametrize(
    "df",
    [
        DataFrame(a=[]),
        DataFrame(a=[]).group_by(),
        DataFrame(a=[]).group_by("a"),
        DataFrame(a=[], b=[], c=[]).group_by("a", "b"),
        DataFrame(a=[], b=[], c=[]).group_by("a").group_by("b"),
    ],
)
def test_one_argument_functions_on_rowless_data_frame_with_summarize(name, df):
    actual = df.group_by().summarize(x=f"{name}(a)")
    expected = df.mutate(x="a")
    assert actual == expected
