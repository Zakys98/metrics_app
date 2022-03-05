
import enum


class Categories(enum.Enum):
    SIGNED = 0
    UNSIGNED = 1
    POINTER = 2


class TypeResolver:

    def __init__(self) -> None:
        self.types = {Categories.SIGNED: dict(), Categories.UNSIGNED: dict(),
                      Categories.POINTER: dict()}

    def loadTypes(self, filename: str) -> None:
        with open(filename) as file:
            lines = file.readlines()
        for line in lines:
            self.__parseLine(line)

    def __parseLine(self, line: str) -> None:
        line = line.strip().split(':')
        line[1] = line[1]
        if(line[0] == 'unsigned' or line[0] == 'unsigned long'):
            self.types[Categories.UNSIGNED][line[0]] = line[1]
        elif(line[0] == 'void *'):
            self.types[Categories.POINTER][line[0]] = line[1]
        else:
            self.types[Categories.SIGNED][line[0]] = line[1]

    def getType(self, line: str, size: str):
        if(line[-1] == '*'):
            return self.getKey(Categories.POINTER, '8')
        elif(line == 'unsigned' or line == 'unsigned long'):
            return self.getKey(Categories.UNSIGNED, size)
        return self.getKey(Categories.SIGNED, size)

    def getKey(self, category, val):
        for key, value in self.types[category].items():
            if val == value:
                return key
        raise KeyError('Key does not exist')
