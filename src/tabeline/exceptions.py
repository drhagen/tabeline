class TabelineError(Exception):
    pass


class NonexistentColumnError(TabelineError):
    def __init__(self, column: str):
        super().__init__(column)
        self.column = column

    def __str__(self) -> str:
        return f"Cannot perform this operation using nonexistent column {self.column}"


class DuplicateColumnError(TabelineError):
    def __init__(self, column: str):
        super().__init__(column)
        self.column = column

    def __str__(self) -> str:
        return f"Column {self.column} is duplicated."


class RenameExistingError(TabelineError):
    def __init__(self, old_column: str, new_column: str):
        super().__init__(old_column, new_column)
        self.old_column = old_column
        self.new_column = new_column

    def __str__(self) -> str:
        return (
            f"Cannot rename {self.old_column} to {self.new_column} because"
            f" {self.new_column} already exists"
        )


class HasGroupsError(TabelineError):
    def __str__(self) -> str:
        return "Cannot perform this operation on a data frame with any group levels"


class NoGroupsError(TabelineError):
    def __str__(self) -> str:
        return "Cannot perform this operation on a data frame with no group levels"


class GroupColumnError(TabelineError):
    def __init__(self, column: str):
        super().__init__(column)
        self.column = column

    def __str__(self) -> str:
        return f"Cannot perform this operation on group column {self.column}"


class RowlessDataFrameError(TabelineError):
    def __str__(self) -> str:
        return "Cannot perform this operation on a data frame with no rows"


class IndexOutOfRangeError(TabelineError):
    def __init__(self, index: int, length: int):
        self.index = index
        self.length = length

    def __str__(self) -> str:
        return f"Cannot index element {self.index} from data frame with {self.length} rows"


class UnmatchedColumnsError(TabelineError):
    def __init__(self, expected_columns: tuple[str, ...], actual_columns: tuple[str, ...]):
        super().__init__(expected_columns, actual_columns)
        self.expected_columns = expected_columns
        self.actual_columns = actual_columns

    def __str__(self) -> str:
        return (
            "Columns do not match\n"
            f"Expected columns: {list(self.expected_columns)}\n"
            f"Actual columns: {list(self.actual_columns)}"
        )


class UnmatchedGroupLevelsError(TabelineError):
    def __init__(
        self,
        expected_group_levels: tuple[tuple[str, ...], ...],
        actual_group_levels: tuple[tuple[str, ...], ...],
    ):
        super().__init__(expected_group_levels, actual_group_levels)
        self.expected_group_levels = expected_group_levels
        self.actual_group_levels = actual_group_levels

    def __str__(self) -> str:
        expected_str = ",".join(
            "[" + ",".join(level) + "]" for level in self.expected_group_levels
        )
        actual_str = ",".join("[" + ",".join(level) + "]" for level in self.actual_group_levels)
        return f"Group levels do not match; expected {expected_str} but got {actual_str}"


class UnmatchedHeightError(TabelineError):
    def __init__(self, expected_height: int, actual_height: int):
        super().__init__(expected_height, actual_height)
        self.expected_height = expected_height
        self.actual_height = actual_height

    def __str__(self) -> str:
        return (
            f"Heights do not match; expected {self.expected_height} but got {self.actual_height}"
        )


class NotSameError(TabelineError):
    def __init__(self, column: tuple[object, ...]):
        super().__init__(column)
        self.column = column

    def __str__(self) -> str:
        used = set()
        unique_elements = [x for x in self.column if x not in used and (used.add(x) or True)]
        return f"Assertion that all elements are the same failed, found {unique_elements}"
