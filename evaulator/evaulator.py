from ctypes import cdll
import matplotlib.pyplot as plt


def syscallNameLoader(fileName : str) -> list:
    listOfNames = list()
    with open(fileName, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            listOfNames.append(line[0:-1])
    return listOfNames

def readNoData(fileName : str) -> dict:
    dictOfNames = dict()
    size = mylib.getSizeOfEnumTypes()
    with open(fileName, 'rb') as file:
        while True:
            byte = file.read(size)
            if not byte:
                break
            type = int.from_bytes(byte, "little")
            if(type in dictOfNames):
                dictOfNames[type] = dictOfNames[type] + 1
            else:
                dictOfNames[type] = 1
    return dictOfNames

def sortDictonary(dict : dict) -> dict:
    return sorted(dict.items(), key=lambda x: x[1], reverse=True)

def showHistogram(myDictionary):
    ax = plt.axes()
    students = list()
    for key, value in dictOfNames.items():
        lal = len('sys_enter_')
        students.append(listOfNames[key][lal:])
    print(students)
    ax.set_xlabel('Syscall names')
    ax.set_ylabel('Number of calls')
    #figure(figsize=(13, 8), dpi=100)
    plt.bar(students, myDictionary.values(), width=0.5)
    plt.show()

if __name__ == '__main__':
    mylib = cdll.LoadLibrary('./build/libevaulator.so')

    listOfNames = syscallNameLoader('build/syscall_names')
    dictOfNames = readNoData('../build/output.bin')
    #dictOfNames = sortDictonary(dictOfNames)
    dictOfNames.pop(67)
    dictOfNames = {key: val for key, val in dictOfNames.items() if val > 1000}
    showHistogram(dictOfNames)
