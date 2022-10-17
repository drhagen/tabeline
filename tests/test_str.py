from tabeline import DataTable


def test_str():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    _ = str(table)


def test_str_grouped():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x", "y")
    _ = str(table)


def test_str_multiple_level_grouped():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x").group_by("y")
    _ = str(table)


def test_repr():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    _ = str(table)


def test_repr_grouped():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x", "y")
    _ = str(table)


def test_repr_multiple_level_grouped():
    table = DataTable(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x").group_by("y")
    _ = str(table)
