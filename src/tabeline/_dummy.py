__all__ = ["dummy_name", "dummy_frame"]

import polars as pl

dummy_name = "_dummy"


def dummy_frame(height: int) -> pl.DataFrame:
    # Lots of things in Polars don't work if the DataFrame has no columns
    # This constructs an effectively columnless data frame with the correct height
    return pl.DataFrame({dummy_name: pl.repeat(False, height, eager=True)})
