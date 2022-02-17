#ifndef __MAIN_H__
#define __MAIN_H__

#include "syscall_enum.h"

/*struct Data {
    enum Types type;
    pid_t pid;
};*/

//#define SYS_ENTER_SOCKET_STRUCTLEN 156
//#define SYS_ENTER_SOCKET_SOCKERPAIR_STRUCTLEN 146

#define GETLEN(x) x##_LEN

#define FUNC(x) \
    struct mynice_##x { \
        enum Types type; \
        char data[GETLEN(x)]; \
    };

FUNC(SYS_ENTER_SOCKET)

struct sys_enter_userspace {
    enum Types type;
};


struct Data {
    enum Types type;
    pid_t pid;
    char data[20];
};

#endif