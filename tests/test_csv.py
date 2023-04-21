import tempfile
from pathlib import Path

import pytest

from tabeline import DataFrame


@pytest.mark.parametrize(
    "df",
    [
        DataFrame(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True]),
        DataFrame(escape=["a a", "c,c", r"s\s", 'q"q', "q'q", "n\nn"]),
    ],
)
def test_csv_roundtrip(df):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory).joinpath("temp.csv")
        df.write_csv(path)
        actual = DataFrame.read_csv(path)
    assert actual == df
