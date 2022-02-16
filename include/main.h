#ifndef __MAIN_H__
#define __MAIN_H__

#include "syscall_enum.h"

struct Data {
    enum Types type;
    pid_t pid;
    char filename[32];
};

struct sys_enter_sendto_t {
    enum Types type;
	int unusedParams;
	int __syscall_nr;
	long fd;
	int buff;
	long len;
	long flags;
	int addr;
	long addr_len;
};

#endif