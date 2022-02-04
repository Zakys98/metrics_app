
import enum

class Types(enum.Enum):
    INT = 0
    CHAR = 1

class Parameter:
    
    def __init__(self, type: Types, name: str) -> None:
        self.type = type
        self.name = name