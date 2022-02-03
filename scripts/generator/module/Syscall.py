

class Syscall:

    def __init__(self, line: str) -> None:
        self.name = line.split(' ')[1].strip()

    def addUnusedParameter(self, list: list) -> None:
        i = 0
        for line in list:
            print(f'{i} {line}')
            i += 1

    def addParameters(self, list: list) -> None:
        i = 0
        for line in list:
            print(f'{i} {line}')
            i += 1

    def getSize(line: str) -> int:
        pass

    def __str__(self) -> str:
        return self.name