#ifndef __MAIN_H__
#define __MAIN_H__

#include "syscall_enum.h"

struct Data {
    enum Types type;
    pid_t pid;
    char filename[32];
};

#endif