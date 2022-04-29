import argparse

def argParserInit():
    parser = argparse.ArgumentParser(description='Syscall generator')
    parser.add_argument('-n', '--name', type=str,
                        help='name of the input file',
                        required=True)
    parser.add_argument('--hist', action='store_true',
                        help='show histogram')
    parser.add_argument('--graph', action='store_true',
                        help='show diferencial graph')
    parser.add_argument('--count', action='store_true',
                        help='count all syscalls')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--data', action='store_true',
                       help='parses syscalls with their data')
    group.add_argument('--no-data', action='store_true',
                       help='parses syscalls without their data')
    return parser.parse_args()