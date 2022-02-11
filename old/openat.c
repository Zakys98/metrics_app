#include <linux/sched.h>

BPF_PERF_OUTPUT(openat);
BPF_PERF_OUTPUT(write);
BPF_PERF_OUTPUT(read);

struct data_t {
    u32 pid;
    char comm[TASK_COMM_LEN];
};

struct sys_enter_openat_t {
    uint64_t unused;

    u32 _nr;
    u64 dfd;
    char *filename;
    u64 flags;
    u64 mode;
};

int sys_enter_opentat_fn(struct sys_enter_openat_t *args) {

    struct data_t data = {};
    u32 pid = (u32)(bpf_get_current_pid_tgid() >> 32);

    data.pid = pid;
    bpf_probe_read_str(data.comm, TASK_COMM_LEN, args->filename);
    //bpf_trace_printk("Openat works %d \\n", pid);

    openat.perf_submit(args, &data, sizeof(data));

    return 0;
}


struct sys_enter_write_t {
    uint64_t unused;
    u32 _nr;
    u64 fd;
    char *buf;
    u64 count;
};

int sys_enter_write_fn(struct sys_enter_write_t *args){

    struct data_t data = {};
    u32 pid = (u32)(bpf_get_current_pid_tgid() >> 32);

    data.pid = pid;
    bpf_probe_read_str(data.comm, TASK_COMM_LEN, args->buf);
    //bpf_trace_printk("Write works %d \\n", pid);

    write.perf_submit(args, &data, sizeof(data));

    return 0;
}


struct sys_enter_read_t {
    uint64_t unused;
    u32 _nr;
    u64 fd;
    char *buf;
    u64 count;
};

int sys_enter_read_fn(struct sys_enter_read_t *args){

    struct data_t data = {};
    u32 pid = (u32)(bpf_get_current_pid_tgid() >> 32);

    data.pid = pid;
    bpf_probe_read_str(data.comm, TASK_COMM_LEN, args->buf);
    //bpf_trace_printk("Read works %d \\n", pid);

    read.perf_submit(args, &data, sizeof(data));

    return 0;
}