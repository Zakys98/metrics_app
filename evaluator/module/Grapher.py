from turtle import color
import matplotlib.pyplot as plt


class Grapher:

    def __init__(self, listOfSyscallNames : list, parsedSyscalls : dict) -> None:
        """
        Constructor

        param listOfSyscallNames: list with syscall names
        param parsedSyscalls: dict with syscalls
        """
        self.listOfSyscallNames = listOfSyscallNames
        self.parsedSyscalls = parsedSyscalls
        self.epollWait = listOfSyscallNames.index('SYS_ENTER_EPOLL_WAIT')

    def sortDictionary(self, dict : dict) -> dict:
        """
        Sort dictionary in descending order

        param dict: input dict
        return: sorted dict
        """
        return sorted(dict.items(), key=lambda item: item[1], reverse=True)

    def __countAllSyclass(self) -> dict:
        """
        Count how many times were each syscall called

        return: dict with counted syscall
        """
        countedSyscalls = dict()
        for key, value in self.parsedSyscalls.items():
            for key, val in value.items():
                if(key in countedSyscalls):
                    countedSyscalls[key] = countedSyscalls[key] + val
                else:
                    countedSyscalls[key] = val
        return countedSyscalls

    def countSyscalls(self) -> None:
        """
        Print how many times were all syscall called
        """
        syscalls = self.__countAllSyclass()
        num = 0
        for _, value in syscalls.items():
            num = num + value
        print(f'Number of called syscalls: {num}')

    def calledSyscall(self) -> None:
        """
        Print how many times were each syscall called
        """
        syscalls = self.__countAllSyclass()
        for name, value in self.sortDictionary(syscalls):
            lenght = len(self.listOfSyscallNames[name])
            name = self.listOfSyscallNames[name] + ' ' * (28 - lenght)
            print(f'{name}: {value}')


    def showHistogram(self) -> None:
        """
        Show histogram with syscalls which were called more than 1000
        """
        syscalls = self.__countAllSyclass()
        syscalls = {key: val for key, val in syscalls.items() if val > 1000}
        syscalls.pop(self.epollWait)
        ax = plt.axes()
        remainingSyscalls = list()
        for key, _ in syscalls.items():
            strip = len('sys_enter_')
            try:
                remainingSyscalls.append(self.listOfSyscallNames[key][strip:])
            except:
                print('Bad usage of --data or --no-data argument')
                exit(1)
        ax.set_xlabel('Syscall names')
        ax.set_ylabel('Number of calls')
        plt.title('Histogram')
        plt.bar(remainingSyscalls, syscalls.values(), width=0.5)
        plt.show()

    def showDifirencialGraph(self) -> None:
        """
        Show diferencial graph with syscalls which were called more than 1000
        """
        times = list(i for i in range(len(self.parsedSyscalls)))
        syscalls = self.__countAllSyclass()
        syscalls = {key: val for key, val in syscalls.items() if val > 1000}
        syscalls.pop(self.epollWait)
        for key in syscalls:
            syscall = list()
            for _, calls in self.parsedSyscalls.items():
                if (key not in calls):
                    syscall.append(0)
                else:
                    syscall.append(calls[key])
            plt.plot(times, syscall, label=self.listOfSyscallNames[key])
        plt.ylabel('Number of calls')
        plt.xlabel('Seconds')
        plt.title('Diferencial graph')
        plt.legend()
        plt.show()