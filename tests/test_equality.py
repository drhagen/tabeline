from tabeline import DataTable


def test_tables_are_equal():
    first = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    second = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    assert first == second


def test_tables_are_not_equal():
    first = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    second = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 10.1])
    assert first != second


def test_table_equal_to_itself():
    table = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    assert table == table


def test_empty_tables_are_equal():
    first = DataTable()
    second = DataTable()
    assert first == second


def test_empty_table_equal_to_itself():
    table = DataTable()
    assert table == table


def test_rowless_table_equal():
    first = DataTable(x=[], y=[], z=[])
    second = DataTable(x=[], y=[], z=[])
    assert first == second


def test_rowless_table_equal_to_itself():
    table = DataTable(x=[], y=[], z=[])
    assert table == table


def test_columnless_tables_are_equal():
    first = DataTable.columnless(height=6)
    second = DataTable.columnless(height=6)
    assert first == second


def test_columnless_table_equal_to_itself():
    table = DataTable.columnless(height=6)
    assert table == table


def test_reordered_rows_are_not_equal():
    first = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    second = DataTable(x=[1, 2, 4, 3], y=[True, False, True, True], z=[3.5, 2.2, 8.9, 6.7])
    assert first != second


def test_reordered_columns_are_not_equal():
    first = DataTable(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    second = DataTable(x=[1, 2, 3, 4], z=[3.5, 2.2, 6.7, 8.9], y=[True, False, True, True])
    assert first != second


def test_grouped_tables_are_equal():
    first = DataTable(
        x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9]
    ).group_by("x")
    second = DataTable(
        x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9]
    ).group_by("x")
    assert first == second


def test_grouped_tables_with_differnt_levels_are_not_equal():
    first = DataTable(
        x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9]
    ).group_by("x")
    second = DataTable(
        x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9]
    ).group_by("y")
    assert first != second
