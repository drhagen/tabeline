from tabeline import Array


def test_equals():
    array1 = Array(0, 1, 2)
    array2 = Array(0, 1, 2)
    assert array1 == array2
