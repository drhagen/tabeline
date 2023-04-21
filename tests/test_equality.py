from tabeline import DataFrame


def test_data_frames_are_equal():
    first = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    second = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    assert first == second


def test_data_frames_are_not_equal():
    first = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    second = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 10.1])
    assert first != second


def test_data_frame_equal_to_itself():
    df = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    assert df == df


def test_empty_data_frames_are_equal():
    first = DataFrame()
    second = DataFrame()
    assert first == second


def test_empty_data_frame_equal_to_itself():
    df = DataFrame()
    assert df == df


def test_rowless_data_frame_equal():
    first = DataFrame(x=[], y=[], z=[])
    second = DataFrame(x=[], y=[], z=[])
    assert first == second


def test_rowless_data_frame_equal_to_itself():
    df = DataFrame(x=[], y=[], z=[])
    assert df == df


def test_columnless_data_frames_are_equal():
    first = DataFrame.columnless(height=6)
    second = DataFrame.columnless(height=6)
    assert first == second


def test_columnless_data_frame_equal_to_itself():
    df = DataFrame.columnless(height=6)
    assert df == df


def test_reordered_rows_are_not_equal():
    first = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    second = DataFrame(x=[1, 2, 4, 3], y=[True, False, True, True], z=[3.5, 2.2, 8.9, 6.7])
    assert first != second


def test_reordered_columns_are_not_equal():
    first = DataFrame(x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9])
    second = DataFrame(x=[1, 2, 3, 4], z=[3.5, 2.2, 6.7, 8.9], y=[True, False, True, True])
    assert first != second


def test_grouped_data_frames_are_equal():
    first = DataFrame(
        x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9]
    ).group_by("x")
    second = DataFrame(
        x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9]
    ).group_by("x")
    assert first == second


def test_grouped_data_frames_with_different_levels_are_not_equal():
    first = DataFrame(
        x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9]
    ).group_by("x")
    second = DataFrame(
        x=[1, 2, 3, 4], y=[True, False, True, True], z=[3.5, 2.2, 6.7, 8.9]
    ).group_by("y")
    assert first != second
