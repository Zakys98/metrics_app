#include <stdio.h>
#include <time.h>

#include "helper.h"
#include "evallib.h"

int getSyscallSize(int pos){
    size_t over = sizeof(syscallSize) / sizeof(syscallSize[0]);
    if (pos > over)
        return -1;
    return syscallSize[pos];
}

int getSizeOfEnumTypes(){
    return ENUM_TYPES_LEN;
}

int getSizeOfTime(){
    return sizeof(time_t);
}