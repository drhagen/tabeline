from tabeline import DataFrame


def test_attributes():
    df = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    assert df.height == 4
    assert df.width == 3
    assert df.shape == (4, 3)
    assert df.column_names == ("x", "y", "z")


def test_attributes_empty():
    df = DataFrame()
    assert df.height == 0
    assert df.width == 0
    assert df.shape == (0, 0)
    assert df.column_names == ()


def test_attributes_columnless():
    df = DataFrame.columnless(height=6)
    assert df.height == 6
    assert df.width == 0
    assert df.shape == (6, 0)
    assert df.column_names == ()


def test_attributes_rowless():
    df = DataFrame(x=[], y=[], z=[])
    assert df.height == 0
    assert df.width == 3
    assert df.shape == (0, 3)
    assert df.column_names == ("x", "y", "z")
