from tabeline import DataTable


def test_spread():
    table = DataTable(
        grades=[0, 0, 1, 1, 2, 2], sex=["M", "F", "M", "F", "M", "F"], count=[8, 9, 9, 10, 6, 9]
    )
    actual = table.group("sex").spread("grades", "count")
    expected = DataTable.from_dict({"sex": ["M", "F"], "0": [8, 9], "1": [9, 10], "2": [6, 9]})
    assert actual == expected
