
from .TypeResolver import TypeResolver
from .Parameter import Parameter, Types


class Syscall:

    def __init__(self, line: str, typeResolver: TypeResolver) -> None:
        self.name = line.split(' ')[1].strip()
        self.parameters = list()
        self.typeResolver = typeResolver

    def __str__(self) -> str:
        output = f'struct {self.name} ' + '{\n'
        for parameter in self.parameters:
            output += f'\t{parameter.__str__()};\n'
        output += '};\n\n'
        return output

    def addUnusedParameter(self, list: list) -> None:
        self.parameters.append(Parameter('long', 'unusedParams'))

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
        size = self.__getSizeOfParameter(list[2])
        type = self.typeResolver.getType(line, size)
        self.parameters.append(Parameter(type, name))

    def __getNameOfParameter(self, line: str) -> str:
        return line.pop()

    def __getSizeOfParameter(self, line: str) -> str:
        return line.split(':')[1]

    def __getTypeOfParameter(self, line: str, size: str) -> str:
        resolvedType = {
            ('int', '4'): Types.INT,
            ('int', '8'): Types.LONG,
            ('long', '8'): Types.LONG,
            ('pid_t', '8'): Types.LONG,
            ('umode_t', '8'): Types.LONG,
            ('unsigned', '8'): Types.LONG,
            ('unsignedint', '8'): Types.LONG,
            ('unsignedlong', '8'): Types.LONG,
            ('size_t', '8'): Types.LONG,
            ('char', '1'): Types.CHAR,
            ('constchar*', '8'): Types.CHAR_POINTER,
            ('char*', '8'): Types.CHAR_POINTER,
        }.get((''.join(line), size), Types.UNKNOWN)
        if(resolvedType == Types.UNKNOWN):
            print(f'{line} {size}')
        return resolvedType
