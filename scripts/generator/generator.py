#!/usr/bin/python3

import argparse
import glob
from typing import Type

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
    group.add_argument('--main', action='store_true',
                       help='generates main.h file')
    return parser.parse_args()


def globSyscalls(pattern: str):
    return glob.iglob(f'/sys/kernel/tracing/events/syscalls/{pattern}/format')


if __name__ == "__main__":
    args = argParserInit()
    typeResolver = TypeResolver()
    typeResolver.loadTypes('sizes')
    syscallParser = SyscallParser(f'{args.name}.h', typeResolver)
    for syscall in globSyscalls(args.pattern):
        with open(syscall, "r") as file:
            syscallParser.addSyscall(file.readlines())

    if(args.structure):
        syscallParser.generateStructureFile()
    elif(args.enum):
        syscallParser.generateEnumFile()
    elif(args.main):
        syscallParser.generateMainHFile()
