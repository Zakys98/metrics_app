#!/usr/bin/python3

import argparse
import glob
from os.path import exists

from module.SyscallParser import SyscallParser
from module.TypeResolver import TypeResolver


def argParserInit():
    parser = argparse.ArgumentParser(description='Syscall generator')
    parser.add_argument('-p', '--pattern', type=str, metavar='WORD',
                        help='matching pattern in glob',
                        required=True)
    parser.add_argument('-n', '--name', type=str,
                        help='name of the output file',
                        required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--structure', action='store_true',
                       help='generates file with syscalls structures')
    group.add_argument('--enum', action='store_true',
                       help='generates file with syscalls enum')
    group.add_argument('--user', action='store_true',
                       help='generates file with user space structures')
    group.add_argument('--bpf', action='store_true',
                       help='generates file with bpf program')
    group.add_argument('--bpf_without_data', action='store_true',
                       help='generates file with bpf program which send only types')
    group.add_argument('--handler', action='store_true',
                       help='generates file with handler function')
    group.add_argument('--handler_without_data', action='store_true',
                       help='generates file with handler function which resolves only types of syscalls')
    group.add_argument('--helper', action='store_true',
                       help='generates file with array with lenght of syscalls and array with names of syscalls')
    group.add_argument('--syscall_name', action='store_true',
                       help='generates file with names of syscalls')
    return parser.parse_args()


def fileExists(filename: str):
    return exists(filename)


def globSyscalls(pattern: str):
    return glob.iglob(f'/sys/kernel/tracing/events/syscalls/{pattern}/format')


if __name__ == "__main__":
    args = argParserInit()
    typeResolver = TypeResolver()
    if not(fileExists('sizes')):
        print('File with sizes of data type called sizes does not exist')
        exit()
    typeResolver.loadTypes('sizes')
    syscallParser = SyscallParser(args.name, typeResolver)
    for syscall in globSyscalls(args.pattern):
        with open(syscall, "r") as file:
            syscallParser.addSyscall(file.readlines())

    if(args.structure):
        syscallParser.generateStructureFile()
    elif(args.enum):
        syscallParser.generateEnumFile()
    elif(args.user):
        syscallParser.generateUserFile()
    elif(args.bpf):
        syscallParser.generateBpfFile()
    elif(args.bpf_without_data):
        syscallParser.generateBpfWithoutDataFile()
    elif(args.handler):
        syscallParser.generateHandlerFile()
    elif(args.handler_without_data):
        syscallParser.generateHandlerWithoutDataFile()
    elif(args.helper):
        syscallParser.generateHelperFile()
    elif(args.syscall_name):
        syscallParser.generateSyscallNamesFile()
