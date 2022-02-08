
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
        self.__getSizeOfParameter(list[2])
        print(list)

    def __getSizeOfParameter(self, line: str) -> int:
        print(line)

    def __str__(self) -> str:
        return self.name