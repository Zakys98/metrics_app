#!/usr/bin/python3

import argparse
import glob

from module.SyscallParser import SyscallParser

def argParserInit():
    parser = argparse.ArgumentParser(description='Syscall generator')
    parser.add_argument('-p', '--pattern', type=str, metavar='WORD', help='matching pattern in glob', required=True)
    parser.add_argument('-n', '--name', type=str, help='name of the output file', default='syscall_structures.h')
    return parser.parse_args()

def globSyscalls(pattern : str):
    return glob.iglob(f'/sys/kernel/tracing/events/syscalls/{pattern}/format')

if __name__ == "__main__":
    args = argParserInit()
    syscallParser = SyscallParser()
    for syscall in globSyscalls(args.pattern):
        with open(syscall, "r") as file:
            syscallParser.addSyscall(file.readlines())

    syscallParser.generateFile(args.name)