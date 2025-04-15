import pytest

from tabeline import Array, DataFrame, Record


@pytest.mark.parametrize(
    ("column", "exact_type"),
    [
        ([True, False], bool),
        ([0, 1], int),
        ([0.0, 1.0], float),
        (["0", "1"], str),
        (["0", None], type(None)),
    ],
)
def test_scalar_indexing(column, exact_type):
    df = DataFrame(x=column)
    actual = df[1, "x"]
    assert type(actual) is exact_type
    assert actual == column[1]


def test_single_column_indexing():
    df = DataFrame(x=[0.0, 1.0], y=["a", "b"])
    actual = df[:, "x"]
    assert actual == Array(0.0, 1.0)


def test_single_column_subsetted_with_slice():
    df = DataFrame(x=[0.0, 1.0, 2.0, 4.0], y=["a", "b", "c", "d"])
    actual = df[1:3, "x"]
    assert actual == Array(1.0, 2.0)


def test_single_column_subsetted_with_sequence():
    df = DataFrame(x=[0.0, 1.0, 2.0, 4.0], y=["a", "b", "c", "d"])
    actual = df[[0, 2], "y"]
    assert actual == Array("a", "c")


def test_single_row_indexing():
    df = DataFrame(x=[0.0, 1.0], y=["a", "b"])
    actual = df[1, :]
    assert actual == Record(x=1.0, y="b")


def test_single_row_subsetted_with_sequence():
    df = DataFrame(x=[0.0, 1.0], y=["a", "b"], z=[True, False])
    actual = df[1, ["x", "z"]]
    assert actual == Record(x=1.0, z=False)


def test_table_indexing_noop():
    df = DataFrame(x=[0.0, 1.0, 2.0, 4.0], y=["a", "b", "c", "d"])
    actual = df[:, :]
    assert actual == df


def test_table_indexing_with_column_sequence():
    df = DataFrame(x=[0.0, 1.0, 2.0, 4.0], y=["a", "b", "c", "d"], z=[True, False, True, False])
    actual = df[:, ["x", "z"]]
    assert actual == DataFrame(x=[0.0, 1.0, 2.0, 4.0], z=[True, False, True, False])


def test_table_indexing_with_row_slice():
    df = DataFrame(x=[0.0, 1.0, 2.0, 4.0], y=["a", "b", "c", "d"])
    actual = df[1:3, :]
    assert actual == DataFrame(x=[1.0, 2.0], y=["b", "c"])


def test_table_indexing_with_row_slice_and_column_sequence():
    df = DataFrame(x=[0.0, 1.0, 2.0, 4.0], y=["a", "b", "c", "d"], z=[True, False, True, False])
    actual = df[1:3, ["x", "z"]]
    assert actual == DataFrame(x=[1.0, 2.0], z=[False, True])


def test_table_indexing_with_sequence_and_slice():
    df = DataFrame(x=[0.0, 1.0, 2.0, 4.0], y=["a", "b", "c", "d"])
    actual = df[[0, 2], :]
    assert actual == DataFrame(x=[0.0, 2.0], y=["a", "c"])


def test_table_indexing_with_sequence_and_sequence():
    df = DataFrame(x=[0.0, 1.0, 2.0, 4.0], y=["a", "b", "c", "d"], z=[True, False, True, False])
    actual = df[[0, 2], ["x", "z"]]
    assert actual == DataFrame(x=[0.0, 2.0], z=[True, True])
