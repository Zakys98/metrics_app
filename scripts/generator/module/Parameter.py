
import enum


class Types(enum.Enum):
    UNKNOWN = 0
    INT = 1
    CHAR = 2
    CHAR_POINTER = 3


class Parameter:

    def __init__(self, type: Types, name: str, size: int) -> None:
        self.type = type
        self.name = name
        self.size = size

    def __str__(self) -> str:
        return str(f'{self.convert(self.type)} {self.name}')

    @staticmethod
    def convert(type: Types) -> str:
        return {
            Types.UNKNOWN: 'int',
            Types.INT: 'int',
            Types.CHAR: 'char',
            Types.CHAR_POINTER: 'char *'
        }[type]
