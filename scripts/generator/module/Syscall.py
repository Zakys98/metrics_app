
from .Parameter import Parameter, Types

class Syscall:

    def __init__(self, line: str) -> None:
        self.name = line.split(' ')[1].strip()
        self.parameters = list()

    def addUnusedParameter(self, list: list) -> None:
        self.parameters.append(Parameter(Types.INT ,'unused'))

    def addParameters(self, list: list) -> None:
        for line in list:
            self.__parseLine(line)

    def __parseLine(self, line: str) -> None:
        list = line.replace('\t', '').split(';')
        list.pop()
        if not list:
            return
        print(list)
        type, name = self.__getTypeAndName(list[0])
        size = self.__getSizeOfParameter(list[2])
        print(f'{type} {name} {size}')

    def __getTypeAndName(self, line: str) -> tuple:
        line = line.split(':')[1].split(' ')
        name = line.pop()    
        for x in line:
            type = {
                'int': Types.INT,
                'char': Types.CHAR,
                '*': Types.CHAR_POINTER
            }.get(x, Types.UNKNOWN)
        return type, name

    def __getSizeOfParameter(self, line: str) -> int:
        return line.split(':')[1]

    def __str__(self) -> str:
        return self.name