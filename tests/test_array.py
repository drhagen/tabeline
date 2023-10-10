import numpy as np
import polars as pl

from tabeline import Array


def test_equals():
    array1 = Array(0, 1, 2)
    array2 = Array(0, 1, 2)
    assert array1 == array2


def test_polars_equals():
    array1 = Array(0, 1, 2)
    array2 = pl.Series([0, 1, 2])
    assert array1 == array2


def test_numpy_equals():
    array1 = Array(0, 1, 2)
    array2 = np.array([0, 1, 2])
    assert array1 == array2
