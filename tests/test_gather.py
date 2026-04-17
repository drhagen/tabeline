from tabeline import DataFrame


def test_gather():
    df = DataFrame.from_dict({"sex": ["M", "F"], "0": [8, 9], "1": [9, 10], "2": [6, 9]})
    actual = df.gather("grades", "count", "0", "1", "2")
    expected = DataFrame(
        sex=["M", "F", "M", "F", "M", "F"],
        grades=["0", "0", "1", "1", "2", "2"],
        count=[8, 9, 9, 10, 6, 9],
    ).group_by("sex")
    assert actual == expected


def test_gather_multiple_index_columns():
    df = DataFrame.from_dict(
        {"country": ["US", "US"], "sex": ["M", "F"], "0": [8, 9], "1": [9, 10]}
    )
    actual = df.gather("grades", "count", "0", "1")
    expected = DataFrame(
        country=["US", "US", "US", "US"],
        sex=["M", "F", "M", "F"],
        grades=["0", "0", "1", "1"],
        count=[8, 9, 9, 10],
    ).group_by("country", "sex")
    assert actual == expected


def test_gather_existing_group_levels():
    df = DataFrame.from_dict(
        {"country": ["US", "US"], "sex": ["M", "F"], "0": [8, 9], "1": [9, 10]}
    ).group_by("country")
    actual = df.gather("grades", "count", "0", "1")
    expected = (
        DataFrame(
            country=["US", "US", "US", "US"],
            sex=["M", "F", "M", "F"],
            grades=["0", "0", "1", "1"],
            count=[8, 9, 9, 10],
        )
        .group_by("country")
        .group_by("sex")
    )
    assert actual == expected


def test_gather_rowless():
    df = DataFrame.from_dict({"sex": [], "0": [], "1": []})
    actual = df.gather("grades", "count", "0", "1")
    expected = DataFrame(sex=[], grades=[], count=[]).group_by("sex")
    assert actual == expected


def test_gather_empty_group_level():
    df = DataFrame.from_dict({"sex": ["M", "F"], "0": [8, 9], "1": [9, 10]}).group_by()
    actual = df.gather("grades", "count", "0", "1")
    expected = (
        DataFrame(
            sex=["M", "F", "M", "F"],
            grades=["0", "0", "1", "1"],
            count=[8, 9, 9, 10],
        )
        .group_by()
        .group_by("sex")
    )
    assert actual == expected
