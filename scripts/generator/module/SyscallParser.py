
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

    def __enumStructLen(self) -> str:
        output = ''
        for syscall in self.syscalls:
            output += f'#define {syscall.name.upper()}_LEN ' \
                      f'sizeof(struct {syscall.name}) \n'
        output += '\n'
        return output

    def __enumFooter(self) -> str:
        output = '};\n\n' \
                 '#endif // __SYSCALL_ENUM_H__'
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

    def generateUserFile(self) -> None:
        with open(self.name, 'w') as file:
            file.write(self.__userHeader())
            file.write(self.__userStruct())
            for syscall in self.syscalls:
                file.write(f'STRUCT({syscall.name.upper()})\n')
            file.write(self.__userFooter())

    def __userHeader(self) -> str:
        output = '#ifndef __MAIN_H__\n' \
                 '#define __MAIN_H__\n\n' \
                 '#include "syscall_enum.h"\n\n'
        return output

    def __userStruct(self) -> str:
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
        return '\n#endif // __MAIN_H__'

    def generateBpfFile(self) -> None:
        with open(self.name, 'w') as file:
            file.write(self.__bpfHeader())
            file.write(self.__bpfMacroFunction())
            for syscall in self.syscalls:
                file.write(f'FUNCTION({syscall.name}, {syscall.name.upper()})\n')
            file.write(self.__bpfFooter())

    def __bpfHeader(self) -> str:
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

    def __bpfFooter(self) -> str:
        return '\nchar LICENSE[] SEC("license") = "GPL";'

    def generateHandlerFile(self) -> str:
        with open(self.name, 'w') as file:
            file.write(self.__handlerHeader())
            for syscall in self.syscalls:
                file.write(f'\t\tcase {syscall.name.upper()}:\n')
                file.write(f'\t\t\tloggerLog(body, {syscall.name.upper()}_LEN);\n')
                file.write('\t\t\tbreak;\n')
            file.write(self.__handlerFooter())

    def __handlerHeader(self) -> str:
        output = '#include <stdio.h>\n\n' \
                 '#include <handler.h>\n\n' \
                 '#include <logger.h>\n' \
                 '#include <syscall_enum.h>\n' \
                 '#include <user.h>\n\n' \
                 'int handle(void *ctx, void *data, size_t size) {\n' \
                 '\tstruct user_type *type = (struct user_type *)data;\n' \
                 '\tloggerLog(&type->type, sizeof(enum Types));\n' \
                 '\tchar *body = (char *)data + sizeof(enum Types);\n' \
                 '\tswitch(type->type){\n'
        return output

    def __handlerFooter(self) -> str:
        output = '\t}\n' \
                 '\treturn 0;\n' \
                 '}\n'
        return output

    def generateHelperFile(self) -> None:
        with open(self.name, 'w') as file:
            file.write(self.__helperHeader())
            file.write(self.__helperArrayLenght())
            file.write(self.__helperArrayName())

    def __helperHeader(self) -> str:
        output = '#pragma once\n\n' \
                 '#include "syscall_enum.h"\n\n'
        return output

    def __helperArrayLenght(self) -> str:
        output = 'static int syscallSize[] = {\n'
        for syscall in self.syscalls:
                output += f'\t{syscall.name.upper()}_LEN,\n'
        output = output[:-2]
        output += '\n};\n\n'
        return output

    def __helperArrayName(self) -> str:
        output = 'static char syscallName[][50] = {\n'
        for syscall in self.syscalls:
                output += f'\t"{syscall.name.upper()}",\n'
        output = output[:-2]
        output += '\n};\n\n'
        return output