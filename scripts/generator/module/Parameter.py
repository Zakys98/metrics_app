
import enum

class Types(enum.Enum):
    UNKNOWN = 0
    INT = 1
    CHAR = 2
    CHAR_POINTER = 3

class Parameter:
    
    def __init__(self, type: Types, name: str) -> None:
        self.type = type
        self.name = name