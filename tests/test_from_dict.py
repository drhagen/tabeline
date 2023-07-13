import pytest

from tabeline import Array, DataFrame


@pytest.mark.parametrize(
    "data",
    [
        {"x": [0, 1, 2], "y": ["a", "b", "c"]},
        {"x": Array(0, 1, 2), "y": Array("a", "b", "c")},
    ],
)
def test_from_dict(data):
    df = DataFrame(x=[0, 1, 2], y=["a", "b", "c"])
    assert DataFrame.from_dict(data) == df


@pytest.mark.parametrize(
    "data",
    [
        {"x": [], "y": []},
        {"x": Array(), "y": Array()},
    ],
)
def test_from_dict_rowless(data):
    df = DataFrame(x=[], y=[])
    assert DataFrame.from_dict(data) == df


def test_to_dict_rowless():
    df = DataFrame(x=[], y=[])
    assert df.to_dict() == {"x": Array(), "y": Array()}


def test_from_dict_to_dict_empty():
    data = {}
    df = DataFrame()
    assert DataFrame.from_dict(data) == df
    assert df.to_dict() == data


def test_to_dict():
    df = DataFrame(x=[0, 1, 2], y=["a", "b", "c"])
    assert df.to_dict() == {"x": Array(0, 1, 2), "y": Array("a", "b", "c")}
