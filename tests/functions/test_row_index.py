import pytest

from tabeline import DataFrame
from tabeline.exceptions import FunctionArgumentCountError


def test_row_index0_rejects_any_args():
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="row_index0(x)")

    error = exc_info.value
    assert error.function == "row_index0"
    assert error.expected == 0
    assert error.actual == 1


def test_row_index1_rejects_any_args():
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="row_index1(x)")

    error = exc_info.value
    assert error.function == "row_index1"
    assert error.expected == 0
    assert error.actual == 1
