from tabeline import DataFrame


def test_str():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    _ = str(df)


def test_str_grouped():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x", "y")
    _ = str(df)


def test_str_multiple_level_grouped():
    df = (
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
        .group_by("x")
        .group_by("y")
    )
    _ = str(df)


def test_repr():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
    _ = str(df)


def test_repr_grouped():
    df = DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"]).group_by("x", "y")
    _ = str(df)


def test_repr_multiple_level_grouped():
    df = (
        DataFrame(x=[0, 0, 1], y=[True, False, True], z=["a", "b", "c"])
        .group_by("x")
        .group_by("y")
    )
    _ = str(df)
