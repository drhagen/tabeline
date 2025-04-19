__all__ = ["concatenate_columns", "concatenate_rows"]

from . import _tabeline
from ._data_frame import DataFrame


def concatenate_columns(data_frame: DataFrame, *data_frames: DataFrame) -> DataFrame:
    return DataFrame(
        _tabeline.concatenate_columns(
            data_frame._py_data_frame, [df._py_data_frame for df in data_frames]
        )
    )


def concatenate_rows(data_frame: DataFrame, *data_frames: DataFrame) -> DataFrame:
    return DataFrame(
        _tabeline.concatenate_rows(
            data_frame._py_data_frame, [df._py_data_frame for df in data_frames]
        )
    )
