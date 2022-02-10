
from .Syscall import Syscall


class SyscallParser:

    def __init__(self) -> None:
        self.syscalls = list()

    def addSyscall(self, syscallList: str) -> None:
        syscall = Syscall(syscallList[0])
        syscall.addUnusedParameter(syscallList[3:7])
        syscall.addParameters(syscallList[8:])
        self.syscalls.append(syscall)
        # print(syscall)

    def generateFile(self, outputName: str) -> None:
        with open(outputName, 'w') as file:
            file.write('\n')
            for syscall in self.syscalls:
                file.write(syscall.__str__())
