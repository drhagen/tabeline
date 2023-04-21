class TabelineException(Exception):
    pass


class NonexistentColumn(TabelineException):
    def __init__(self, column: str):
        super().__init__(column)
        self.column = column

    def __str__(self) -> str:
        return f"Cannot perform this operation using nonexistent column {self.column}"


class DuplicateColumn(TabelineException):
    def __init__(self, column: str):
        super().__init__(column)
        self.column = column

    def __str__(self) -> str:
        return f"Column {self.column} is duplicated."


class RenameExisting(TabelineException):
    def __init__(self, old_column: str, new_column: str):
        super().__init__(old_column, new_column)
        self.old_column = old_column
        self.new_column = new_column

    def __str__(self) -> str:
        return (
            f"Cannot rename {self.old_column} to {self.new_column} because"
            f" {self.new_column} already exists"
        )


class HasGroups(TabelineException):
    def __str__(self) -> str:
        return "Cannot perform this operation on a data frame with any group levels"


class NoGroups(TabelineException):
    def __str__(self) -> str:
        return "Cannot perform this operation on a data frame with no group levels"


class GroupColumn(TabelineException):
    def __init__(self, column: str):
        super().__init__(column)
        self.column = column

    def __str__(self) -> str:
        return f"Cannot perform this operation on group column {self.column}"


class RowlessDataFrame(TabelineException):
    def __str__(self) -> str:
        return "Cannot perform this operation on a data frame with no rows"


class IndexOutOfRange(TabelineException):
    def __init__(self, index: int, length: int):
        self.index = index
        self.length = length

    def __str__(self) -> str:
        return f"Cannot index element {self.index} from data frame with {self.length} rows"
