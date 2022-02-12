from tabeline import DataTable


def test_inner_join():
    table1 = DataTable(x=[0, 1, 2, 3], y=["a", "b", "c", "d"])
    table2 = DataTable(x=[3, 2, 1, 0], z=["a", "b", "c", "d"])

    actual = table1.inner_join(table2)

    expected = DataTable(x=[0, 1, 2, 3], y=["a", "b", "c", "d"], z=["d", "c", "b", "a"])

    assert actual == expected


def test_inner_join_ignore_unmatched():
    table1 = DataTable(x=[0, 1, 2, 3, 4], y=["a", "b", "c", "d", "e"])
    table2 = DataTable(x=[3, 2, -1, 1, 0], z=["a", "b", "z", "c", "d"])

    actual = table1.inner_join(table2)

    expected = DataTable(x=[0, 1, 2, 3], y=["a", "b", "c", "d"], z=["d", "c", "b", "a"])

    assert actual == expected
