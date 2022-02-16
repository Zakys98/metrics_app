
from .TypeResolver import TypeResolver
from .Syscall import Syscall


class SyscallParser:

    def __init__(self, outputName: str, typeResolver: TypeResolver) -> None:
        self.name = outputName
        self.syscalls = list()
        self.typeResolver = typeResolver

    def addSyscall(self, syscallList: str) -> None:
        syscall = Syscall(syscallList[0], self.typeResolver)
        syscall.addUnusedParameter(syscallList[3:7])
        syscall.addParameters(syscallList[8:])
        self.syscalls.append(syscall)

    def generateEnumFile(self) -> None:
        with open(self.name, 'w') as file:
            file.write(self.__enumHeader())
            for syscall in self.syscalls:
                file.write(f'\t{syscall.name.upper()},\n')
            file.write(self.__enumFooter())

    def __enumHeader(self):
        output = '#ifndef __SYSCALL_ENUM_H__\n' \
                 '#define __SYSCALL_ENUM_H__\n\n' \
                 'enum Types {\n'
        return output

    def __enumFooter(self):
        output = '};\n\n' \
                 '#endif // __SYSCALL_ENUM_H__'
        return output

    def generateStructureFile(self) -> None:
        with open(self.name, 'w') as file:
            file.write(self.__structuresHeader())
            for syscall in self.syscalls:
                file.write(syscall.__str__())
            file.write(self.__structuresFooter())

    def __structuresHeader(self):
        output = '#ifndef __SYSCALL_STRUCTURES_H__\n' \
                 '#define __SYSCALL_STRUCTURES_H__\n\n'
        return output

    def __structuresFooter(self):
        return '#endif // __SYSCALL_STRUCTURES_H__'
