import pytest

from tabeline import DataFrame
from tabeline.exceptions import FunctionArgumentCountError


def test_n_rejects_any_args():
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="n(x)")

    error = exc_info.value
    assert error.function == "n"
    assert error.expected == 0
    assert error.actual == 1
