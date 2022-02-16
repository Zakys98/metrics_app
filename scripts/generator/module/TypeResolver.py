
import enum


class Categories(enum.Enum):
    SIGNED = 0
    UNSIGNED = 1
    POINTER = 2

class TypeResolver:

    def __init__(self) -> None:
        self.types = {Categories.SIGNED: list(), Categories.UNSIGNED: list(), Categories.POINTER: list()}

    def loadTypes(self, filename: str) -> None:
        with open(filename) as file:
            lines = file.readlines()
        for line in lines:
            self.__parseLine(line)
        #print(self.types)

    def __parseLine(self, line: str) -> None:
        line = line.strip().split(':')
        line[1] = int(line[1])
        if(line[0] == 'unsigned' or line[0] == 'unsigned long'):
            self.types[Categories.UNSIGNED].append((line[0], line[1]))
        elif(line[0] == 'pointer'):
            self.types[Categories.POINTER].append((line[0], line[1]))
        else:
            self.types[Categories.SIGNED].append((line[0], line[1]))

    def getType(self, line: str, size: str):
        pass
