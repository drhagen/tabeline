import math

import numpy as np
import polars as pl
import pytest
from polars.testing import assert_series_equal

from tabeline import Array, DataType

# Skip some types, otherwise there are too many tests
numeric_types = [
    DataType.Integer8,
    # DataType.Integer16,
    # DataType.Integer32,
    DataType.Integer64,
    DataType.Whole8,
    # DataType.Whole16,
    # DataType.Whole32,
    DataType.Whole64,
    DataType.Float32,
    DataType.Float64,
]

float_types = [
    DataType.Float32,
    DataType.Float64,
]


@pytest.mark.parametrize(
    "elements",
    [
        [],
        [0],
        [None, None, None],
        [0, None, 2],
        [True, False, None],
        [None, "b", "c"],
        [-math.inf, math.inf, math.nan, None],
    ],
)
def test_equals(elements):
    array1 = Array(*elements)
    array2 = Array(*elements)
    assert array1 == array2


def test_not_equal_to_nan():
    assert Array(0.0, 1.0, None) != Array(0.0, 1.0, math.nan)


def test_not_equal_to_null():
    assert Array(0.0, 1.0, None) != Array(0.0, 1.0, 2.0)


@pytest.mark.parametrize("type_1", numeric_types)
def test_equals_typed_integer_and_untyped(type_1):
    array1 = Array[type_1](0, 1, 2)
    array2 = Array(0, 1, 2)
    assert array1 == array2


def test_polars_equals():
    array1 = Array(0, 1, None)
    array2 = pl.Series([0, 1, None])
    assert array1 == array2


@pytest.mark.parametrize(
    "elements",
    [[], [0, 1, 2], [-math.inf, math.inf, math.nan], [True, False, True], ["a", "b", "c"]],
)
def test_numpy_equals(elements):
    array1 = Array(*elements)
    array2 = np.array(elements)
    assert array1 == array2


@pytest.mark.parametrize("type_1", float_types)
def test_equals_typed_float_and_untyped(type_1):
    # Use simple values that are equal in 32 and 64 bits
    array1 = Array[type_1](0, 1.5, -2.25)
    array2 = Array(0, 1.5, -2.25)
    assert array1 == array2


@pytest.mark.parametrize("type_1", numeric_types)
@pytest.mark.parametrize("type_2", numeric_types)
def test_equals_typed_integer(type_1, type_2):
    array1 = Array[type_1](0, 1, 2)
    array2 = Array[type_2](0, 1, 2)
    assert array1 == array2


@pytest.mark.parametrize("type_1", float_types)
@pytest.mark.parametrize("type_2", float_types)
def test_equals_typed_float(type_1, type_2):
    array1 = Array[type_1](0, 1.5, -2.25)
    array2 = Array[type_2](0, 1.5, -2.25)
    assert array1 == array2


@pytest.mark.parametrize("elements", [[], [0], [0, 1, 2], [True, False, True], ["a", "b", "c"]])
def test_array_iter(elements):
    array = Array(*elements)
    assert list(array) == elements


def test_incompatible_type():
    with pytest.raises(
        TypeError,
        match=(
            "Expected data_type to be compatible with DataType.Integer64, "
            "but got DataType.String"
        ),
    ):
        _ = Array(0, 1, 2, data_type=DataType.String)


@pytest.mark.parametrize("elements", [[], [0], [0, 1, 2], [True, False, True], ["a", "b", "c"]])
def test_from(elements):
    expected = Array(*elements)

    assert expected == Array.from_sequence(elements)
    assert elements == list(expected)

    series = pl.Series(values=elements)
    assert expected == Array.from_polars(series)
    assert_series_equal(series, expected.to_polars())

    numpy_array = np.array(elements)
    assert expected == Array.from_numpy(numpy_array)
    assert all(numpy_array == expected.to_numpy())


@pytest.mark.parametrize("elements", [[0, None, 2], [None, False, True], ["a", "b", None]])
def test_from_none(elements):
    expected = Array(*elements)

    assert expected == Array.from_sequence(elements)
    assert elements == list(expected)

    series = pl.Series(values=elements)
    assert expected == Array.from_polars(series)
    assert series.equals(expected.to_polars())


@pytest.mark.parametrize("elements", [[], [None, None, None]])
def test_from_all_nones(elements):
    # This test is needed because Polars defaults to Float32 instead of Null
    # when all elements are None
    expected = Array(*elements)

    assert expected == Array.from_sequence(elements)
    assert elements == list(expected)

    series = pl.Series(values=elements, dtype=pl.Null)
    assert expected == Array.from_polars(series)
    assert series.equals(expected.to_polars())


def test_str_repr():
    # Only verify that it doesn't crash
    array = Array(0, 1, 2)
    _ = str(array)
    _ = repr(array)
