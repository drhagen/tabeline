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


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("to_boolean(1)", True),
        ("to_boolean(-1)", True),
        ("to_boolean(0)", False),
        ("to_boolean(1.0)", True),
    ],
)
def test_cast_boolean_literal(expression, expected):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=[expected])
    assert actual == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("to_integer(2)", 2),
        ("to_integer(-3)", -3),
        ("to_integer(2.5)", 2),
    ],
)
def test_cast_integer_literal(expression, expected):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=[expected])
    assert actual == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("to_float(2)", 2.0),
        ("to_float(-3)", -3.0),
        ("to_float(2.5)", 2.5),
    ],
)
def test_cast_float_literal(expression, expected):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=[expected])
    assert actual == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("to_string(2)", "2"),
        ("to_string(-3)", "-3"),
        ("to_string(2.5)", "2.5"),
    ],
)
def test_cast_string_literal(expression, expected):
    df = DataFrame.columnless(1)
    actual = df.mutate(result=expression)
    expected = DataFrame(result=[expected])
    assert actual == expected
