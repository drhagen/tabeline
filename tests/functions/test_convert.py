import pytest

from tabeline import DataFrame


@pytest.mark.parametrize(
    "values",
    [
        (0, -1, 4),
        (0.0, -1.0, 4.0),
        (True, False, True),
    ],
)
def test_cast_boolean(values):
    df = DataFrame(a=values)
    actual = df.transmute(b="to_boolean(a)")
    expected = DataFrame(b=[bool(value) for value in values])
    assert actual == expected


@pytest.mark.parametrize(
    "values",
    [
        (0, -1, 4),
        (0.0, -1.0, 4.0),
        (True, False, True),
        ("0", "-1", "4"),
    ],
)
def test_cast_integer(values):
    df = DataFrame(a=values)
    actual = df.transmute(b="to_integer(a)")
    expected = DataFrame(b=[int(value) for value in values])
    assert actual == expected


@pytest.mark.parametrize(
    "values",
    [
        (0, -1, 4),
        (0.0, -1.0, 4.0),
        (True, False, True),
        ("0.0", "-1.5", "4", "3.2e-4"),
    ],
)
def test_cast_float(values):
    df = DataFrame(a=values)
    actual = df.transmute(b="to_float(a)")
    expected = DataFrame(b=[float(value) for value in values])
    assert actual == expected


@pytest.mark.parametrize(
    "values",
    [
        (0, -1, 4),
        (0.0, -1.0, 4.0),
        ("0.0", "-1.5", "4", "3.2e-4"),
    ],
)
def test_cast_string(values):
    df = DataFrame(a=values)
    actual = df.transmute(b="to_string(a)")
    expected = DataFrame(b=[str(value) for value in values])
    assert actual == expected
