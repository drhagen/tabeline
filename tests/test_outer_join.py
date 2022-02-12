from tabeline import DataTable


def test_outer_join():
    table1 = DataTable(x=[0, 1, 2, 3], y=["a", "b", "c", "d"])
    table2 = DataTable(x=[3, 2, 1, 0], z=["a", "b", "c", "d"])

    actual = table1.outer_join(table2)

    expected = DataTable(x=[0, 1, 2, 3], y=["a", "b", "c", "d"], z=["d", "c", "b", "a"])

    assert actual == expected


def test_outer_join_unmatched():
    table1 = DataTable(x=[0, 1, 2, 3, 4], y=["a", "b", "c", "d", "e"])
    table2 = DataTable(x=[3, 2, -1, 1, 0], z=["a", "b", "z", "c", "d"])

    actual = table1.outer_join(table2)

    expected = DataTable(
        x=[-1, 0, 1, 2, 3, 4], y=[None, "a", "b", "c", "d", "e"], z=["z", "d", "c", "b", "a", None]
    )

    assert actual == expected
