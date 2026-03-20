import pytest

from tabeline import DataFrame, DataType
from tabeline.exceptions import TypeMismatchError


@pytest.mark.parametrize(
    ("values", "expected_type"),
    [
        ([1, 2, 3], DataType.Integer64),
        (["a", "b", "c"], DataType.String),
    ],
)
def test_not_rejects_non_boolean(values, expected_type):
    df = DataFrame(x=values)

    with pytest.raises(TypeMismatchError) as exc_info:
        df.filter("~x")

    assert exc_info.value == TypeMismatchError("~_", DataType.Boolean, expected_type)
