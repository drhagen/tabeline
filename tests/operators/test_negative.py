import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import NumericTypeNotSatisfiedError


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        (["a", "b", "c"], DataType.String),
        ([True, False, True], DataType.Boolean),
    ],
)
def test_negative_rejects_non_numeric(values, expected_type):
    df = DataFrame(x=values)

    with pytest.raises(NumericTypeNotSatisfiedError) as exc_info:
        df.mutate(y="-x")

    error = exc_info.value
    assert error.operation == "-_"
    assert error.actual == expected_type
