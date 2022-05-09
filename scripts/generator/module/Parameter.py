
import enum


class Types(enum.Enum):
    UNKNOWN = 'unsigned'
    INT = 'int'
    LONG = 'u64'
    CHAR = 'char'
    CHAR_POINTER = 'char *'


class Parameter:

    def __init__(self, type: Types, name: str) -> None:
        """
        Constructor

        param type: type of the parameter
        param name: name of the parameter
        """
        self.type = type
        self.name = name

    def __str__(self) -> str:
        """
        Creates string from object

        return: string
        """
        return f'{self.type} {self.name}'
