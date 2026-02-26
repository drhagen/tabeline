import pytest

from tabeline import DataFrame
from tabeline.exceptions import FunctionArgumentCountError


def test_row_index0_rejects_any_args():
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="row_index0(x)")

    assert exc_info.value == FunctionArgumentCountError("row_index0", 0, 1)


def test_row_index1_rejects_any_args():
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="row_index1(x)")

    assert exc_info.value == FunctionArgumentCountError("row_index1", 0, 1)
