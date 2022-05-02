from turtle import color
import matplotlib.pyplot as plt


class Grapher:

    def __init__(self, listOfSyscallNames : list, parsedSyscalls : dict) -> None:
        self.listOfSyscallNames = listOfSyscallNames
        self.parsedSyscalls = parsedSyscalls

    def sortDictonary(dict : dict) -> dict:
        return sorted(dict.items(), key=lambda x: x[1], reverse=True)

    def __countAllSyclass(self, syscallWithSeconds):
        newDict = dict()
        for key, value in syscallWithSeconds.items():
            for key, val in value.items():
                if(key in newDict):
                    newDict[key] = newDict[key] + val
                else:
                    newDict[key] = val
        return newDict

    def countSyscalls(self) -> None:
        syscalls = self.__countAllSyclass(self.parsedSyscalls)
        num = 0
        for _, value in syscalls.items():
            num = num + value
        print(f'Number of called syscalls: {num}')

    def showHistogram(self) -> None:
        syscalls = self.__countAllSyclass(self.parsedSyscalls)
        syscalls = {key: val for key, val in syscalls.items() if val > 1000}
        syscalls.pop(67)
        ax = plt.axes()
        remainingSyscalls = list()
        for key, _ in syscalls.items():
            strip = len('sys_enter_')
            remainingSyscalls.append(self.listOfSyscallNames[key][strip:])
        ax.set_xlabel('Syscall names')
        ax.set_ylabel('Number of calls')
        plt.title('Histogram')
        plt.bar(remainingSyscalls, syscalls.values(), width=0.5)
        plt.show()

    def showDifirencialGraph(self) -> None:
        times = list(i for i in range(len(self.parsedSyscalls)))
        syscalls = self.__countAllSyclass(self.parsedSyscalls)
        syscalls = {key: val for key, val in syscalls.items() if val > 1000}
        syscalls.pop(67)
        for key in syscalls:
            ls = list()
            for _, calls in self.parsedSyscalls.items():
                ls.append(calls[key])
            plt.plot(times, ls, label=self.listOfSyscallNames[key])
        plt.ylabel('Number of calls')
        plt.xlabel('Seconds')
        plt.title('Diferencial graph')
        plt.legend()
        plt.show()