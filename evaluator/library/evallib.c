#include <stdio.h>

#include "helper.h"
#include "evallib.h"

int getSyscallSize(int pos){
    return syscallSize[pos];
}

int getSizeOfEnumTypes(){
    return ENUM_TYPES_LEN;
}
