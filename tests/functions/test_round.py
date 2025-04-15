from tabeline import DataFrame


def test_floor():
    values = [1.2, 2.7, -1.8, None]
    expected = [1.0, 2.0, -2.0, None]
    df = DataFrame(x=values)
    actual = df.mutate(x="floor(x)")
    assert actual == DataFrame(x=expected)


def test_ceil():
    values = [1.2, 2.7, -1.8, None]
    expected = [2.0, 3.0, -1.0, None]
    df = DataFrame(x=values)
    actual = df.mutate(x="ceil(x)")
    assert actual == DataFrame(x=expected)
