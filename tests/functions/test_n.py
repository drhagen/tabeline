import pytest

from tabeline import DataFrame
from tabeline.exceptions import FunctionArgumentCountError


def test_n_rejects_any_args():
    df = DataFrame(x=[1, 2, 3])

    with pytest.raises(FunctionArgumentCountError) as exc_info:
        df.mutate(y="n(x)")

    assert exc_info.value == FunctionArgumentCountError("n", 0, 1)
