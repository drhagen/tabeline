import math

import pytest

from tabeline import Array, DataType
from tabeline.exceptions import IncompatibleElementTypeError

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


@pytest.mark.parametrize(
    ("elements", "data_type"),
    [
        ([None, None, None], DataType.Nothing),
        ([True, True, False], DataType.Boolean),
        (["a", "b", "c"], DataType.String),
    ],
)
def test_from_nonnumeric_data_type(elements, data_type):
    array = Array[data_type](*elements)
    assert array.data_type == data_type

    # With Nones
    array = Array[data_type](None, *elements, None)
    assert array.data_type == data_type


@pytest.mark.parametrize("data_type", numeric_types)
def test_from_numeric_data_type(data_type):
    array = Array[data_type](0, 1, 2)
    assert array.data_type == data_type

    # With Nones
    array = Array[data_type](None, 1, 2, 3, None)
    assert array.data_type == data_type


@pytest.mark.parametrize(
    "data_type", [DataType.Nothing, DataType.Boolean, *numeric_types, DataType.String]
)
def test_from_empty(data_type):
    array = Array[data_type]()
    assert array.data_type == data_type
    assert [] == list(array)


@pytest.mark.parametrize(
    ("elements", "expected_data_type"),
    [
        ([True, True, False], DataType.Boolean),
        ([0, 1, 2], DataType.Integer64),
        ([1.0, 2, 3.0], DataType.Float64),
        ([1, 2.0, 3.0], DataType.Float64),
        ([-math.inf, math.inf, math.nan], DataType.Float64),
        (["a", "b", "c"], DataType.String),
    ],
)
def test_data_type_inference(elements, expected_data_type):
    array = Array(*elements)
    assert array.data_type == expected_data_type

    # With None in front
    array = Array(None, *elements)
    assert array.data_type == expected_data_type

    # With None in middle
    array = Array(*elements, None, *elements)
    assert array.data_type == expected_data_type

    # with None in back
    array = Array(*elements, None)
    assert array.data_type == expected_data_type


@pytest.mark.parametrize("elements", [[], [None, None, None]])
def test_data_type_inference_all_nones(elements):
    array = Array(*elements)

    assert array.data_type == DataType.Nothing
    assert elements == list(array)


def test_not_equal_to_nan():
    assert Array(0.0, 1.0, None) != Array(0.0, 1.0, math.nan)


def test_not_equal_to_null():
    assert Array(0.0, 1.0, None) != Array(0.0, 1.0, 2.0)


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


def test_len():
    assert len(Array(0, 1, 2)) == 3


def test_get_item():
    array = Array("a", "b", None)
    assert array[1] == "b"
    assert array[2] is None


def test_get_one_item():
    # Polars behaves differently on single-element string arrays
    array = Array("a")
    assert array[0] == "a"


@pytest.mark.parametrize(
    "elements",
    [[], [0], [0, 1, 2], [True, False, True], ["a", "b", "c"], [None, None, None]],
)
def test_iter(elements):
    array = Array(*elements)
    assert list(array) == elements


def test_incompatible_type():
    with pytest.raises(IncompatibleElementTypeError) as e:
        _ = Array(0, 1, 2, data_type=DataType.String)

    assert e.value == IncompatibleElementTypeError([str, type(None)], 0, 0)


def test_from_sequence():
    array = Array.from_sequence([0, 1, 2])
    assert array == Array(0, 1, 2)


def test_str_repr():
    # Only verify that it doesn't crash
    array = Array(0, 1, 2)
    _ = str(array)
    _ = repr(array)
