#!/usr/bin/python3

import time

from bcc import BPF

write_counter = 0
read_counter = 0

def handle_sys_enter_opanat(cpu, data, size):
    data = bpf["openat"].event(data)
    file = data.comm.decode('UTF-8')
    date = time.strftime("%H:%M:%S")
    print(f'{date} Pid {data.pid} File {file}')


def handle_sys_enter_write(cpu, data, size):
    data = bpf["write"].event(data)
    global write_counter
    write_counter += 1
    #print(f'TRY is {data.pid} and data are {data.comm}')


def handle_sys_enter_read(cpu, data, size):
    data = bpf["read"].event(data)
    global read_counter
    read_counter += 1
    #print(f'Read pid is {data.pid} and data are {data.comm}')


if __name__ == "__main__":
    counter = 0
    bpf = BPF(src_file='openat.c')
    bpf.attach_tracepoint(tp="syscalls:sys_enter_openat", fn_name="sys_enter_opentat_fn")
    bpf.attach_tracepoint(tp="syscalls:sys_enter_write", fn_name="sys_enter_write_fn")
    bpf.attach_tracepoint(tp="syscalls:sys_enter_read", fn_name="sys_enter_read_fn")

    bpf["openat"].open_perf_buffer(handle_sys_enter_opanat)
    bpf["write"].open_perf_buffer(handle_sys_enter_write)
    bpf["read"].open_perf_buffer(handle_sys_enter_read)

    while True:
        try:
            bpf.perf_buffer_poll()
        except KeyboardInterrupt:
            print(f'Write = {write_counter}')
            print(f'Read = {read_counter}')
            exit()