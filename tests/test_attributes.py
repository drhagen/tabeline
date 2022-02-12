from tabeline import DataTable


def test_attributes():
    table = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    assert table.height == 4
    assert table.width == 3
    assert table.shape == (4, 3)
    assert table.column_names == ("x", "y", "z")


def test_attributes_empty():
    table = DataTable()
    assert table.height == 0
    assert table.width == 0
    assert table.shape == (0, 0)
    assert table.column_names == ()


def test_attributes_columnless():
    table = DataTable.columnless(height=6)
    assert table.height == 6
    assert table.width == 0
    assert table.shape == (6, 0)
    assert table.column_names == ()


def test_attributes_rowless():
    table = DataTable(x=[], y=[], z=[])
    assert table.height == 0
    assert table.width == 3
    assert table.shape == (0, 3)
    assert table.column_names == ("x", "y", "z")
