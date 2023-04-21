from tabeline import DataFrame


def test_gather():
    df = DataFrame.from_dict({"sex": ["M", "F"], "0": [8, 9], "1": [9, 10], "2": [6, 9]})
    actual = df.gather("grades", "count", "0", "1", "2")
    expected = DataFrame(
        sex=["M", "F", "M", "F", "M", "F"],
        grades=["0", "0", "1", "1", "2", "2"],
        count=[8, 9, 9, 10, 6, 9],
    ).group_by("grades")
    assert actual == expected
