
import enum


class Types(enum.Enum):
    UNKNOWN = 'unsigned'
    INT = 'int'
    LONG = 'u64'
    CHAR = 'char'
    CHAR_POINTER = 'char *'


class Parameter:

    def __init__(self, type: Types, name: str) -> None:
        self.type = type
        self.name = name

    def __str__(self) -> str:
        return f'{self.type} {self.name}'
