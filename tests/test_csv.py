import tempfile
from pathlib import Path

import pytest

from tabeline import DataTable


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True]),
        DataTable(escape=["a a", "c,c", r"s\s", 'q"q', "q'q", "n\nn"]),
    ],
)
def test_csv_roundtrip(table):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory).joinpath("temp.csv")
        table.write_csv(path)
        actual = DataTable.read_csv(path)
    assert actual == table
