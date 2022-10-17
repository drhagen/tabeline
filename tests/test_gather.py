from tabeline import DataTable


def test_gather():
    table = DataTable.from_dict({"sex": ["M", "F"], "0": [8, 9], "1": [9, 10], "2": [6, 9]})
    actual = table.gather("grades", "count", "0", "1", "2")
    expected = DataTable(
        sex=["M", "F", "M", "F", "M", "F"],
        grades=["0", "0", "1", "1", "2", "2"],
        count=[8, 9, 9, 10, 6, 9],
    ).group_by("grades")
    assert actual == expected
