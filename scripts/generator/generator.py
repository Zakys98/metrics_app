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
    group.add_argument('--handler', action='store_true',
                       help='generates file with handler function')
    return parser.parse_args()

def fileExists(filename: str):
    return exists(filename)

def globSyscalls(pattern: str):
    return glob.iglob(f'/sys/kernel/tracing/events/syscalls/{pattern}/format')


if __name__ == "__main__":
    args = argParserInit()
    typeResolver = TypeResolver()
    typeResolver.loadTypes('sizes')
    if(fileExists(args.name)):
        exit()
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
    elif(args.handler):
        syscallParser.generateHandlerFile()
