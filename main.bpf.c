#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_core_read.h>

#include "syscall_structures.h"
#include "main.h"


struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 256 * 1024);
} ring_buff SEC(".maps");


struct exec_params_t {
    u64 __unused;
    u64 __unused2;

    char *file;
};

SEC("tp/syscalls/sys_enter_execve")
int handle_execve(struct exec_params_t *params)
{
    struct task_struct *task = (struct task_struct*)bpf_get_current_task();
    struct Data *evt = {0};

    evt = bpf_ringbuf_reserve(&ring_buff, sizeof(*evt), 0);
    if (!evt) {
        bpf_printk("ringbuffer not reserved\n");
        return 0;
    }

    evt->pid = BPF_CORE_READ(task, pid);
    bpf_probe_read_user_str(evt->filename, sizeof(evt->filename), params->file);
    evt->type = SYS_ENTER_OPEN_BY_HANDLE_AT;
    bpf_ringbuf_submit(evt, 0);
    bpf_printk("Execve Called\n");
    return 0;
}

SEC("tp/syscalls/sys_enter_open")
int handle_open(struct sys_enter_open *params){
    
    struct task_struct *task = (struct task_struct*)bpf_get_current_task();
    struct Data *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("ringbuffer not reserved\n");
        return 0;
    }

    data->pid = BPF_CORE_READ(task, pid);
    bpf_probe_read_user_str(data->filename, sizeof(data->filename), params->filename);
    data->type = SYS_ENTER_OPEN;
    bpf_ringbuf_submit(data, 0);
    bpf_printk("Open Called\n");

    return 0;
}

SEC("tp/syscalls/sys_enter_openat")
int handle_openat(struct sys_enter_openat *params){
    
    struct task_struct *task = (struct task_struct*)bpf_get_current_task();
    struct Data *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("ringbuffer not reserved\n");
        return 0;
    }

    data->pid = BPF_CORE_READ(task, pid);
    bpf_probe_read_user_str(data->filename, sizeof(data->filename), params->filename);
    data->type = SYS_ENTER_OPENAT;
    bpf_ringbuf_submit(data, 0);
    bpf_printk("Openat Called\n");

    return 0;
}

char LICENSE[] SEC("license") = "GPL";
