
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
            file.write(self.__enumStructLen())
            file.write('enum Types {\n')
            for syscall in self.syscalls:
                file.write(f'\t{syscall.name.upper()},\n')
            file.write(self.__enumFooter())

    def __enumHeader(self) -> str:
        output = '#ifndef __SYSCALL_ENUM_H__\n' \
                 '#define __SYSCALL_ENUM_H__\n\n' \
                 '#include "syscall_structures.h"\n\n'
        return output

    def __enumFooter(self) -> str:
        output = '};\n\n' \
                 '#endif // __SYSCALL_ENUM_H__'
        return output

    def __enumStructLen(self) -> str:
        output = ''
        for syscall in self.syscalls:
            output += f'#define {syscall.name.upper()}_LEN sizeof(struct {syscall.name}) \n'
        output += '\n'
        return output

    def generateStructureFile(self) -> None:
        with open(self.name, 'w') as file:
            file.write(self.__structuresHeader())
            for syscall in self.syscalls:
                file.write(syscall.__str__())
            file.write(self.__structuresFooter())

    def __structuresHeader(self) -> str:
        output = '#ifndef __SYSCALL_STRUCTURES_H__\n' \
                 '#define __SYSCALL_STRUCTURES_H__\n\n'
        return output

    def __structuresFooter(self) -> str:
        return '#endif // __SYSCALL_STRUCTURES_H__'

    def generateMainHFile(self) -> None:
        with open(self.name, 'w') as file:
            file.write(self.__mainHHeader())
            file.write(self.__mainHStruct())
            for syscall in self.syscalls:
                file.write(f'FUNC({syscall.name.upper()})\n')
            file.write(self.__mainHFooter())

    def __mainHHeader(self) -> str:
        output = '#ifndef __MAIN_H__\n' \
                 '#define __MAIN_H__\n\n' \
                 '#include "syscall_enum.h"\n\n'
        return output

    def __mainHStruct(self) -> str:
        output = '#define GETLEN(x) x##_LEN\n\n' \
                 '#define FUNC(x) \\\n' \
                 '\tstruct USER_##x { \\\n' \
                 '\t\tchar data[GETLEN(x)]; \\\n' \
                 '\t};\n\n' \
                 'struct user_type {\n' \
                 '\tenum Types type;\n' \
                 '};\n\n'
        return output

    def __mainHFooter(self) -> str:
        return '\n#endif // __MAIN_H__'
