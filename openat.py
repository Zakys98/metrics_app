#!/usr/bin/python3

from bcc import BPF
from time import sleep

bpf = BPF(src_file='openat.c')
bpf.attach_tracepoint(tp="syscalls:sys_enter_openat", fn_name="sys_enter_opentat_fn")

def handle_sys_enter_opanat(cpu, data, size):
    data = bpf["events"].event(data)
    print(f'Pid is {data.pid} and data are {data.comm}')

def handle_try(cpu, data, size):
    data = bpf["events"].event(data)
    print(f'TRY is {data.pid} and data are {data.comm}')

bpf["events"].open_perf_buffer(handle_sys_enter_opanat)
bpf["try"].open_perf_buffer(handle_try)

while True:
    try:
        bpf.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()