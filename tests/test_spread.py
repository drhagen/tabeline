from tabeline import DataFrame


def test_spread():
    df = DataFrame(
        grades=[0, 0, 1, 1, 2, 2], sex=["M", "F", "M", "F", "M", "F"], count=[8, 9, 9, 10, 6, 9]
    )
    actual = df.group_by("sex").spread("grades", "count")
    expected = DataFrame.from_dict({"sex": ["M", "F"], "0": [8, 9], "1": [9, 10], "2": [6, 9]})
    assert actual == expected
