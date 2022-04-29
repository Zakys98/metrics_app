from ctypes import cdll
from module.ArgumentParser import argParserInit
from module.Grapher import Grapher


def syscallNameLoader(fileName : str) -> list:
    listOfNames = list()
    with open(fileName, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            listOfNames.append(line[0:-1])
    return listOfNames

def readWithData(fileName : str) -> dict:
    print("data")
    exit()
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

def readNoData(fileName : str) -> dict:
    dictOfNames = dict()
    size = mylib.getSizeOfEnumTypes()
    with open(fileName, 'rb') as file:
        while True:
            time = file.read(8)
            byte = file.read(size)
            if not byte:
                break
            time = int.from_bytes(time, "little")
            if(time not in dictOfNames):
                dictOfNames[time] = dict()
            type = int.from_bytes(byte, "little")
            if(type in dictOfNames[time]):
                dictOfNames[time][type] = dictOfNames[time][type] + 1
            else:
                dictOfNames[time][type] = 1
    return dictOfNames


if __name__ == '__main__':
    args = argParserInit()
    mylib = cdll.LoadLibrary('./build/libevaulator.so')
    listOfSyscallNames = syscallNameLoader('build/syscall_names')

    if(args.data):
        parsedSyscalls = readWithData(args.name)
    else:
        parsedSyscalls = readNoData(args.name)

    grapher = Grapher(listOfSyscallNames, parsedSyscalls)
    if(args.hist):
        grapher.showHistogram()
    if(args.count):
        grapher.countSyscalls()
    if(args.graph):
        grapher.showDifirencialGraph()
