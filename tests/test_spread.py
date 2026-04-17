import pytest

from tabeline import DataFrame
from tabeline.exceptions import NoGroupsError


def test_spread():
    df = DataFrame(
        grades=[0, 0, 1, 1, 2, 2], sex=["M", "F", "M", "F", "M", "F"], count=[8, 9, 9, 10, 6, 9]
    )
    actual = df.group_by("sex").spread("grades", "count")
    expected = DataFrame.from_dict({"sex": ["M", "F"], "0": [8, 9], "1": [9, 10], "2": [6, 9]})
    assert actual == expected


def test_spread_multiple_group_levels():
    df = DataFrame(
        country=["US", "US", "US", "US"],
        sex=["M", "F", "M", "F"],
        grades=[0, 0, 1, 1],
        count=[8, 9, 9, 10],
    )
    actual = df.group_by("country").group_by("sex").spread("grades", "count")
    expected = DataFrame.from_dict(
        {"country": ["US", "US"], "sex": ["M", "F"], "0": [8, 9], "1": [9, 10]}
    ).group_by("country")
    assert actual == expected


def test_spread_no_groups():
    df = DataFrame(grades=[0, 0, 1, 1], sex=["M", "F", "M", "F"], count=[8, 9, 9, 10])
    with pytest.raises(NoGroupsError):
        df.spread("grades", "count")


def test_spread_rowless():
    df = DataFrame(grades=[], sex=[], count=[]).group_by("sex")
    actual = df.spread("grades", "count")
    expected = DataFrame(sex=[])
    assert actual == expected


def test_spread_empty_group_level():
    df = (
        DataFrame(sex=["M", "F", "M", "F"], grades=[0, 0, 1, 1], count=[8, 9, 9, 10])
        .group_by()
        .group_by("sex")
    )
    actual = df.spread("grades", "count")
    expected = DataFrame.from_dict({"sex": ["M", "F"], "0": [8, 9], "1": [9, 10]}).group_by()
    assert actual == expected
