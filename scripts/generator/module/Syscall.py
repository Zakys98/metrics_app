
from .Parameter import Parameter, Types


class Syscall:

    def __init__(self, line: str) -> None:
        self.name = line.split(' ')[1].strip()
        self.parameters = list()

    def __str__(self) -> str:
        output = f'struct {self.name} ' + '{\n'
        for parameter in self.parameters:
            output += f'\t{parameter.__str__()};\n'
        output += '};\n\n'
        return output

    def addUnusedParameter(self, list: list) -> None:
        self.parameters.append(Parameter(Types.INT, 'unused', 8))

    def addParameters(self, list: list) -> None:
        for line in list:
            self.__parseLine(line)

    def __parseLine(self, line: str) -> None:
        list = line.replace('\t', '').split(';')
        list.pop()
        if not list:
            return
        type, name = self.__getTypeAndName(list[0])
        size = self.__getSizeOfParameter(list[2])
        self.parameters.append(Parameter(type, name, size))
        # print(f'{type} {name} {size}')

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
