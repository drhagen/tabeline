from tabeline import DataFrame


def test_outer_join():
    df1 = DataFrame(x=[0, 1, 2, 3], y=["a", "b", "c", "d"])
    df2 = DataFrame(x=[3, 2, 1, 0], z=["a", "b", "c", "d"])

    actual = df1.outer_join(df2)

    expected = DataFrame(x=[0, 1, 2, 3], y=["a", "b", "c", "d"], z=["d", "c", "b", "a"])

    assert actual == expected


def test_outer_join_unmatched():
    df1 = DataFrame(x=[0, 1, 2, 3, 4], y=["a", "b", "c", "d", "e"])
    df2 = DataFrame(x=[3, 2, -1, 1, 0], z=["a", "b", "z", "c", "d"])

    actual = df1.outer_join(df2)

    expected = DataFrame(
        x=[0, 1, 2, 3, 4, -1], y=["a", "b", "c", "d", "e", None], z=["d", "c", "b", "a", None, "z"]
    )

    assert actual == expected


def test_match_different_names():
    df1 = DataFrame(x=[0, 1, 2, 3], y=["a", "b", "c", "d"])
    df2 = DataFrame(a=[3, 2, 1, 0], z=["a", "b", "c", "d"])

    actual = df1.outer_join(df2, by=[("x", "a")])

    expected = DataFrame(x=[0, 1, 2, 3], y=["a", "b", "c", "d"], z=["d", "c", "b", "a"])

    assert actual == expected
