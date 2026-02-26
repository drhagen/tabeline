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

    assert exc_info.value == NumericTypeNotSatisfiedError("-_", expected_type)
