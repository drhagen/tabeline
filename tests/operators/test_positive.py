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
def test_positive_rejects_non_numeric(values, expected_type):
    df = DataFrame(x=values)

    with pytest.raises(NumericTypeNotSatisfiedError) as exc_info:
        df.mutate(y="+x")

    assert exc_info.value.operation == "+_"
    assert exc_info.value.actual == expected_type
