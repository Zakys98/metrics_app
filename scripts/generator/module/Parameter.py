
import enum


class Types(enum.Enum):
    UNKNOWN = 0
    INT = 1
    LONG = 2
    CHAR = 3
    CHAR_POINTER = 4


class Parameter:

    def __init__(self, type: Types, name: str, size: int) -> None:
        self.type = type
        self.name = name
        self.size = size

    def __str__(self) -> str:
        return str(f'{self.convertToStr(self.type)} {self.name}')

    @staticmethod
    def convertToTypes(type: str, size: int):
        #if(type == )
        type = {
                'int': Types.INT,
                'char': Types.CHAR,
                '*': Types.CHAR_POINTER
        }.get(type, Types.UNKNOWN)

    @staticmethod
    def convertToStr(type: Types) -> str:
        return {
            Types.UNKNOWN: 'int',
            Types.INT: 'u32',
            Types.LONG: 'u64',
            Types.CHAR: 'char',
            Types.CHAR_POINTER: 'char *'
        }[type]
