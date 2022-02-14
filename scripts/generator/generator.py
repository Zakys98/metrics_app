#!/usr/bin/python3

import argparse
import glob

from module.SyscallParser import SyscallParser


def argParserInit():
    parser = argparse.ArgumentParser(description='Syscall generator')
    parser.add_argument('-p', '--pattern', type=str, metavar='WORD',
                        help='matching pattern in glob',
                        required=True)
    parser.add_argument('-n', '--name', type=str,
                        help='name of the output file',
                        required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--structure', action='store_true', help='generates file with syscalls structures')
    group.add_argument('--enum', action='store_true', help='generates file with syscalls enum')
    return parser.parse_args()


def globSyscalls(pattern: str):
    return glob.iglob(f'/sys/kernel/tracing/events/syscalls/{pattern}/format')


if __name__ == "__main__":
    args = argParserInit()
    syscallParser = SyscallParser(f'{args.name}.h')
    for syscall in globSyscalls(args.pattern):
        with open(syscall, "r") as file:
            syscallParser.addSyscall(file.readlines())

    if(args.structure):
        syscallParser.generateStructureFile()
    elif(args.enum):
        syscallParser.generateEnumFile()
