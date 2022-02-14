#ifndef __MAIN_H__
#define __MAIN_H__

#include "syscall_enum.h"

struct Data {
    pid_t pid;
    char filename[32];
    enum Types type;
};

#endif