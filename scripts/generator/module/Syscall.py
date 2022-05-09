
from .TypeResolver import TypeResolver
from .Parameter import Parameter, Types


class Syscall:

    def __init__(self, line: str, typeResolver: TypeResolver) -> None:
        """
        Constructor

        param line: type of the parameter
        param typeResolver: name of the parameter
        """
        self.name = line.split(' ')[1].strip()
        self.parameters = list()
        self.typeResolver = typeResolver

    def __str__(self) -> str:
        """
        Creates string from object

        return: string
        """
        output = f'struct {self.name} ' + '{\n'
        for parameter in self.parameters:
            output += f'\t{parameter.__str__()};\n'
        output += '};\n\n'
        return output

    def addUnusedParameter(self) -> None:
        """
        Add unused parameter to parameters
        """
        self.parameters.append(Parameter('long', 'unusedParams'))

    def addParameters(self, list: list) -> None:
        """
        Add parameter to parameters

        param list: list of parameters
        """
        for line in list:
            self.__parseLine(line)

    def __parseLine(self, line: str) -> None:
        """
        Split line and add parameter to parameters
        
        param line: string with information about parametr
        """
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
        """
        Get name of parameter
        
        param line: string with information about parametr
        """
        return line.pop()

    def __getSizeOfParameter(self, line: str) -> str:
        """
        Get size of parameter
        
        param line: string with information about parametr
        """
        return line.split(':')[1]
