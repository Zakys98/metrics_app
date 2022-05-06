from ctypes import cdll
from os.path import exists

from module.ArgumentParser import argParserInit
from module.Grapher import Grapher


def syscallNameLoader(fileName : str) -> list:
    """
    Load syscall names

    param fileName: input file
    return: list with syscall names
    """
    listOfNames = list()
    with open(fileName, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            listOfNames.append(line[0:-1])
    return listOfNames

def readData(fileName : str) -> dict:
    """
    Read time, syscall type and syscall information

    param fileName: input file
    return: dict with syscall information
    """
    dictOfNames = dict()
    sizeOfEnum = mylib.getSizeOfEnumTypes()
    with open(fileName, 'rb') as file:
        while True:
            time = file.read(8)
            if not time:
                break
            time = int.from_bytes(time, "little")
            type = file.read(sizeOfEnum)
            if not type:
                break
            if(time not in dictOfNames):
                dictOfNames[time] = dict()
            type = int.from_bytes(type, "little")
            if(type in dictOfNames[time]):
                dictOfNames[time][type] = dictOfNames[time][type] + 1
            else:
                dictOfNames[time][type] = 1
            body = file.read(mylib.getSyscallSize(type))
            if not body:
                break
    return dictOfNames

def readNoData(fileName : str) -> dict:
    """
    Read time and syscall type

    param fileName: input file
    return: dict with syscall information
    """
    dictOfNames = dict()
    sizeOfEnum = mylib.getSizeOfEnumTypes()
    with open(fileName, 'rb') as file:
        while True:
            time = file.read(8)
            type = file.read(sizeOfEnum)
            if not type:
                break
            time = int.from_bytes(time, "little")
            if(time not in dictOfNames):
                dictOfNames[time] = dict()
            type = int.from_bytes(type, "little")
            if(type in dictOfNames[time]):
                dictOfNames[time][type] = dictOfNames[time][type] + 1
            else:
                dictOfNames[time][type] = 1
    return dictOfNames

def fileExists(filename: str) -> bool:
    """
    Checks if file exists

    param fileName: input file
    return: true if exists otherwise false
    """
    return exists(filename)


if __name__ == '__main__':
    args = argParserInit()
    if not(fileExists(args.input)):
        print('Input file does not exist')
        exit()
    if not(fileExists('./build/libevaulator.so')):
        print('Library does not exist')
        exit()
    mylib = cdll.LoadLibrary('./build/libevaulator.so')
    listOfSyscallNames = syscallNameLoader('build/syscall_names')

    if(args.data):
        parsedSyscalls = readData(args.input)
    else:
        parsedSyscalls = readNoData(args.input)

    grapher = Grapher(listOfSyscallNames, parsedSyscalls)
    if(args.count):
        grapher.countSyscalls()
    if(args.called):
        grapher.calledSyscall()
    if(args.hist):
        grapher.showHistogram()
    if(args.graph):
        grapher.showDifirencialGraph()
