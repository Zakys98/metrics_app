from ctypes import cdll
from os.path import exists

from module.ArgumentParser import argParserInit
from module.Grapher import Grapher


def syscallNameLoader(fileName: str) -> list:
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


def readData(fileName: str) -> dict:
    """
    Read time, syscall type and syscall information

    param fileName: input file
    return: dict with syscall information
    """
    dictOfNames = dict()
    sizeOfEnum = library.getSizeOfEnumTypes()
    sizeOfTime = library.getSizeOfTime()
    with open(fileName, 'rb') as file:
        while True:
            time = file.read(sizeOfTime)
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
            sizeOfSyscallStruct = library.getSyscallSize(type)
            if(sizeOfSyscallStruct == -1):
                print('Bad usage of --data or --no-data argument')
                exit(-1)
            body = file.read(sizeOfSyscallStruct)
            if not body:
                break
    return dictOfNames


def readNoData(fileName: str) -> dict:
    """
    Read time and syscall type

    param fileName: input file
    return: dict with syscall information
    """
    dictOfNames = dict()
    sizeOfEnum = library.getSizeOfEnumTypes()
    sizeOfTime = library.getSizeOfTime()
    with open(fileName, 'rb') as file:
        while True:
            time = file.read(sizeOfTime)
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
    libraryName = './build/libevaluator.so'
    if not(fileExists(args.input)):
        print('Input file does not exist')
        exit()
    if not(fileExists(libraryName)):
        print('Library does not exist')
        exit()
    library = cdll.LoadLibrary(libraryName)
    listOfSyscallNames = syscallNameLoader('build/syscall_names')

    if(args.data):
        parsedSyscalls = readData(args.input)
    else:
        parsedSyscalls = readNoData(args.input)

    grapher = Grapher(listOfSyscallNames, parsedSyscalls)
    if(args.hist):
        grapher.showHistogram()
    if(args.graph):
        grapher.showDifirencialGraph()
    if(args.count):
        grapher.countSyscalls()
    if(args.called):
        grapher.calledSyscall()
