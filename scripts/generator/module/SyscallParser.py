
from .TypeResolver import TypeResolver
from .Syscall import Syscall


class SyscallParser:

    def __init__(self, outputName: str, typeResolver: TypeResolver) -> None:
        """
        Constructor

        param outputName: name of the output file
        param typeResolver: resolver of types
        """
        self.name = outputName
        self.syscalls = list()
        self.typeResolver = typeResolver

    def addSyscall(self, syscallList: str) -> None:
        """
        Add syscall

        param syscallList: string with syscall information
        """
        syscall = Syscall(syscallList[0], self.typeResolver)
        syscall.addUnusedParameter()
        syscall.addParameters(syscallList[8:])
        self.syscalls.append(syscall)

    def generateEnumFile(self) -> None:
        """
        Generate enum file
        """
        with open(self.name, 'w') as file:
            file.write(self.__enumHeader())
            file.write(self.__enumStructLen())
            file.write('enum Types {\n')
            for syscall in self.syscalls:
                file.write(f'\t{syscall.name.upper()},\n')
            file.write(self.__enumFooter())

    def __enumHeader(self) -> str:
        """
        Generate header of the enum file
        """
        output = '#ifndef __SYSCALL_ENUM_H__\n' \
                 '#define __SYSCALL_ENUM_H__\n\n' \
                 '#include "syscall_structures.h"\n\n'
        return output

    def __enumStructLen(self) -> str:
        """
        Generate macros of the input structures
        """
        output = ''
        for syscall in self.syscalls:
            output += f'#define {syscall.name.upper()}_LEN ' \
                      f'sizeof(struct {syscall.name}) \n'
        output += '\n'
        return output

    def __enumFooter(self) -> str:
        """
        Generate footer of the enum file
        """
        output = '};\n\n' \
                 '#endif // __SYSCALL_ENUM_H__'
        return output

    def generateStructureFile(self) -> None:
        """
        Generate input structure file
        """
        with open(self.name, 'w') as file:
            file.write(self.__structuresHeader())
            for syscall in self.syscalls:
                file.write(syscall.__str__())
            file.write(self.__structuresFooter())

    def __structuresHeader(self) -> str:
        """
        Generate header of the structure file
        """
        output = '#ifndef __SYSCALL_STRUCTURES_H__\n' \
                 '#define __SYSCALL_STRUCTURES_H__\n\n'
        return output

    def __structuresFooter(self) -> str:
        """
        Generate footer of the structure file
        """
        return '#endif // __SYSCALL_STRUCTURES_H__'

    def generateUserFile(self) -> None:
        """
        Generate file for user space
        """
        with open(self.name, 'w') as file:
            file.write(self.__userHeader())
            file.write(self.__userStruct())
            for syscall in self.syscalls:
                file.write(f'STRUCT({syscall.name.upper()})\n')
            file.write(self.__userFooter())

    def __userHeader(self) -> str:
        """
        Generate header for user space file
        """
        output = '#ifndef __MAIN_H__\n' \
                 '#define __MAIN_H__\n\n' \
                 '#include "syscall_enum.h"\n\n'
        return output

    def __userStruct(self) -> str:
        """
        Generate macro for structures to user space file
        """
        output = '#define GETLEN(x) x##_LEN\n\n' \
                 '#define STRUCT(x) \\\n' \
                 '\tstruct USER_##x { \\\n' \
                 '\t\tenum Types type; \\\n' \
                 '\t\tchar data[GETLEN(x)]; \\\n' \
                 '\t};\n\n' \
                 'struct user_type {\n' \
                 '\tenum Types type;\n' \
                 '};\n\n'
        return output

    def __userFooter(self) -> str:
        """
        Generate footer for user space file
        """
        return '\n#endif // __MAIN_H__'

    def generateBpfFile(self) -> None:
        """
        Generate kernel space file with data
        """
        with open(self.name, 'w') as file:
            file.write(self.__bpfHeader())
            file.write(self.__bpfMacroFunction())
            file.write(self.__bpfMacroGenerate())
            file.write(self.__bpfFooter())

    def __bpfHeader(self) -> str:
        """
        Generate header for kernel space file
        """
        output = '#include "../include/vmlinux.h"\n' \
                 '#include <bpf/bpf_core_read.h>\n' \
                 '#include <bpf/bpf_helpers.h>\n\n' \
                 '#include "../include/user.h"\n' \
                 '#include "../include/syscall_structures.h"\n' \
                 '#include "../include/syscall_enum.h"\n\n' \
                 'struct {\n' \
                 '    __uint(type, BPF_MAP_TYPE_RINGBUF);\n' \
                 '    __uint(max_entries, 256 * 1024);\n' \
                 '} ring_buff SEC(".maps");\n\n'
        return output

    def __bpfMacroFunction(self) -> str:
        """
        Generate macro for function with data in kernel space file
        """
        output = '#define FUNCTION(lower, upper) \\\n' \
                 '\tSEC("tp/syscalls/" #lower "") \\\n' \
                 '\tint handle_##lower(struct lower *params) { \\\n' \
                 '\t\tstruct task_struct *task = (struct task_struct *)bpf_get_current_task(); \\\n' \
                 '\t\tstruct USER_##upper *data = {0}; \\\n' \
                 '\t\tdata = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0); \\\n' \
                 '\t\tif (!data) { \\\n' \
                 '\t\t    bpf_printk("Ringbuffer not reserved\\n"); \\\n' \
                 '\t\t    return 0; \\\n' \
                 '\t\t} \\\n' \
                 '\t\tdata->type = upper; \\\n' \
                 '\t\tbpf_probe_read_kernel(data->data, upper##_LEN, params); \\\n' \
                 '\t\tbpf_ringbuf_submit(data, 0); \\\n' \
                 '\t\treturn 0; \\\n' \
                 '\t}\n\n'
        return output

    def __bpfMacroGenerate(self) -> str:
        """
        Generate functions for every syscall in kernel space file
        """
        output = ''
        for syscall in self.syscalls:
            output += f'FUNCTION({syscall.name}, {syscall.name.upper()})\n'
        return output

    def __bpfFooter(self) -> str:
        """
        Generate footer for kernel space file
        """
        return '\nchar LICENSE[] SEC("license") = "GPL";'

    def generateBpfWithoutDataFile(self) -> str:
        """
        Generate kernel space file without data
        """
        with open(self.name, 'w') as file:
            file.write(self.__bpfHeader())
            file.write(self.__bpfWithoutDataMacroFunction())
            file.write(self.__bpfMacroGenerate())
            file.write(self.__bpfFooter())

    def __bpfWithoutDataMacroFunction(self) -> str:
        """
        Generate macro for function without data in kernel space file
        """
        output = '#define FUNCTION(lower, upper) \\\n' \
                 '\tSEC("tp/syscalls/" #lower "") \\\n' \
                 '\tint handle_##lower(struct lower *params) { \\\n' \
                 '\t\tstruct task_struct *task = (struct task_struct *)bpf_get_current_task(); \\\n' \
                 '\t\tstruct user_type *data = {0}; \\\n' \
                 '\t\tdata = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0); \\\n' \
                 '\t\tif (!data) { \\\n' \
                 '\t\t    bpf_printk("Ringbuffer not reserved\\n"); \\\n' \
                 '\t\t    return 0; \\\n' \
                 '\t\t} \\\n' \
                 '\t\tdata->type = upper; \\\n' \
                 '\t\tbpf_ringbuf_submit(data, 0); \\\n' \
                 '\t\treturn 0; \\\n' \
                 '\t}\n\n'
        return output

    def generateHandlerFile(self) -> None:
        """
        Generate handler function with data file
        """
        with open(self.name, 'w') as file:
            file.write(self.__handlerHeader())
            file.write('\tchar *body = (char *)data + sizeof(enum Types);\n')
            file.write('\tswitch(type->type){\n')
            for syscall in self.syscalls:
                file.write(f'\t\tcase {syscall.name.upper()}:\n')
                file.write(f'\t\t\tloggerLogData(body, {syscall.name.upper()}_LEN);\n')
                file.write('\t\t\tbreak;\n')
            file.write('\t}\n')
            file.write(self.__handlerFooter())

    def __handlerHeader(self) -> str:
        """
        Generate headeer for handler function file
        """
        output = '#include <stdio.h>\n\n' \
                 '#include <handler.h>\n\n' \
                 '#include <logger.h>\n' \
                 '#include <syscall_enum.h>\n' \
                 '#include <user.h>\n\n' \
                 'int handle(void *ctx, void *data, size_t size) {\n' \
                 '\tstruct user_type *type = (struct user_type *)data;\n' \
                 '\tloggerLogType(&type->type, sizeof(enum Types));\n'
        return output

    def __handlerFooter(self) -> str:
        """
        Generate footer for handler function file
        """
        output = '\treturn 0;\n' \
                 '}\n'
        return output

    def generateHandlerWithoutDataFile(self) -> None:
        """
        Generate handler function without data file
        """
        with open(self.name, 'w') as file:
            file.write(self.__handlerHeader())
            file.write(self.__handlerFooter())

    def generateHelperFile(self) -> None:
        """
        Generate helper file for library
        """
        with open(self.name, 'w') as file:
            file.write(self.__helperHeader())
            file.write(self.__helperArrayLenght())

    def __helperHeader(self) -> str:
        """
        Generate header of helper file
        """
        output = '#pragma once\n\n' \
                 '#include "syscall_enum.h"\n\n' \
                 '#define ENUM_TYPES_LEN sizeof(enum Types)\n\n'
        return output

    def __helperArrayLenght(self) -> str:
        """
        Generate array with sizes of structures to helper file
        """
        output = 'static int syscallSize[] = {\n'
        for syscall in self.syscalls:
                output += f'\t{syscall.name.upper()}_LEN,\n'
        output = output[:-2]
        output += '\n};\n\n'
        return output

    def generateSyscallNamesFile(self) -> None:
        """
        Generate syscall names file
        """
        with open(self.name, 'w') as file:
            for syscall in self.syscalls:
                file.write(f'{syscall.name.upper()}\n')