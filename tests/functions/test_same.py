import pytest

from tabeline import DataFrame


@pytest.mark.parametrize(
    "values",
    [
        [True, True],
        [-1, -1],
        ["aa", "aa"],
        [None, None],
    ],
)
def test_same(values):
    df = DataFrame(x=values)
    actual = df.mutate(x="same(x)")
    assert actual == actual


@pytest.mark.parametrize(
    "values",
    [
        [True, True, False],
        [-1, -1, 2],
        ["aa", "aa", "bb"],
        [None, None, 1],
        [None, None, None],
    ],
)
def test_same_group_by(values):
    df = DataFrame(a=[0, 0, 1], x=values)
    actual = df.group_by("a").summarize(x="same(x)")
    expected = DataFrame(a=[0, 1], x=values[1:])
    assert actual == expected


@pytest.mark.parametrize("values", [[0, 1], [0.0, 1.0], ["a", "b"], [1, None]])
def test_same_error(values):
    df = DataFrame(x=values)
    # BaseException because Polars eats the SameError and raises a PyO3 PanicException,
    # which does not inherit from Exception and is not part of the Polars API.
    with pytest.raises(BaseException):  # noqa: B017, PT011
        _ = df.mutate(x="same(x)")


@pytest.mark.parametrize("values", [[0, 1, 2], [0.0, 1.0, 2.0], ["a", "b", "c"], [1, None, 2]])
def test_same_error_group_by(values):
    df = DataFrame(a=[0, 0, 1], x=values)
    # BaseException because Polars eats the SameError and raises a PyO3 PanicException,
    # which does not inherit from Exception and is not part of the Polars API.
    with pytest.raises(BaseException):  # noqa: B017, PT011
        _ = df.group_by("a").summarize(x="same(x)")
