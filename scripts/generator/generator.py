#!/usr/bin/python3

import argparse
import glob

from module.SyscallParser import SyscallParser

def argParserInit():
    parser = argparse.ArgumentParser(description='Syscall generator')
    parser.add_argument('-p', '--pattern', type=str, metavar='word', help='matching pattern in glob', required=True)
    return parser.parse_args()

def globSyscalls(pattern : str):
    return glob.iglob(f'/sys/kernel/tracing/events/syscalls/{pattern}/format')

if __name__ == "__main__":
    args = argParserInit()
    syscallParser = SyscallParser()
    for syscall in globSyscalls(args.pattern):
        with open(syscall, "r") as file:
            syscallParser.addSyscall(file.readlines())