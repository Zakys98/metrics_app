
import enum


class Categories(enum.Enum):
    SIGNED = 0
    UNSIGNED = 1
    POINTER = 2


class TypeResolver:

    def __init__(self) -> None:
        """
        Constructor
        """
        self.types = {Categories.SIGNED: dict(), Categories.UNSIGNED: dict(),
                      Categories.POINTER: dict()}

    def loadTypes(self, filename: str) -> None:
        """
        Loads types from input file

        param filename: input file
        """
        with open(filename) as file:
            lines = file.readlines()
        for line in lines:
            self.__parseLine(line)

    def __parseLine(self, line: str) -> None:
        """
        Parse line of input file

        param line: string with parameter information
        """
        line = line.strip().split(':')
        line[1] = line[1]
        if(line[0] == 'unsigned' or line[0] == 'unsigned long'):
            self.types[Categories.UNSIGNED][line[0]] = line[1]
        elif(line[0] == 'void *'):
            self.types[Categories.POINTER][line[0]] = line[1]
        else:
            self.types[Categories.SIGNED][line[0]] = line[1]

    def getType(self, line: str, size: str):
        """
        Get type of parameter

        param line: string with parameter information
        param size: size of parameter
        """
        if(line[-1] == '*'):
            return self.__getKey(Categories.POINTER, '8')
        elif(line == 'unsigned' or line == 'unsigned long'):
            return self.__getKey(Categories.UNSIGNED, size)
        return self.__getKey(Categories.SIGNED, size)

    def __getKey(self, category: Categories, size: str):
        """
        Get key of parameter

        param category: category of parameter
        param size: size of parameter
        """
        for key, value in self.types[category].items():
            if size == value:
                return key
        raise KeyError('Key does not exist')
