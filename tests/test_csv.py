import tempfile
from pathlib import Path

import pytest

from tabeline import DataTable

from ._xfail import xfail_param


@pytest.mark.parametrize(
    "table",
    [
        DataTable(x=[0, 0, 1], y=["a", "b", "b"], z=[True, False, True]),
        DataTable(escape=["a a", "c,c", r"s\s", 'q"q', "q'q"]),
        # Combine this with the test above once this is fixed
        # https://github.com/pola-rs/polars/issues/4130
        xfail_param(DataTable(escape=["n\nn"])),
    ],
)
def test_csv_roundtrip(table):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory).joinpath("temp.csv")
        table.write_csv(path)
        actual = DataTable.read_csv(path)
    assert actual == table
