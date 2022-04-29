#include <stdio.h>

#include "helper.h"
#include "evallib.h"

int getSyscallSize(int pos){
    return syscallSize[pos];
}

int getSizeOfEnumTypes(){
    return ENUM_TYPES_LEN;
}

char *getSyscallName(int pos){
    printf("C :%s\n", syscallName[pos]);
    return syscallName[pos];
}