
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
        self.parameters.append(Parameter(Types.LONG, 'unused', 8))

    def addParameters(self, list: list) -> None:
        for line in list:
            self.__parseLine(line)

    def __parseLine(self, line: str) -> None:
        list = line.replace('\t', '').split(';')
        list.pop()
        if not list:
            return
        line = list[0].split(':')[1].split(' ')
        name = self.__getNameOfParameter(line)
        type = self.__getTypeofParameter(line)
        size = self.__getSizeOfParameter(list[2])
        self.parameters.append(Parameter(type, name, size))
        # print(f'{type} {name} {size}')

    def __getNameOfParameter(self, line: str) -> str:
        return line.pop()

    def __getTypeofParameter(self, line: str) -> Types:
        print(''.join(line))
        for x in line:
            type = {
                'int': Types.INT,
                'char': Types.CHAR,
                '*': Types.CHAR_POINTER
            }.get(x, Types.UNKNOWN)
        return type

    def __getSizeOfParameter(self, line: str) -> int:
        return line.split(':')[1]
