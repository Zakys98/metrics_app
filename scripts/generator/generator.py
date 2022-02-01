#!/usr/bin/python3

import argparse
import glob

def argParserInit():
    parser = argparse.ArgumentParser(description='Syscall generator')
    parser.add_argument('-p', '--pattern', type=str, metavar='word', help='matching pattern in glob', required=True)
    return parser.parse_args()

def globSyscalls(pattern : str):
    pass

if __name__ == "__main__":
    args = argParserInit()
    for syscall in glob.iglob(f'/sys/kernel/tracing/events/syscalls/{args.pattern}/format'):
        with open(syscall, "r") as file:
            print(file.read())