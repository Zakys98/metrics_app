#include <linux/sched.h>

BPF_PERF_OUTPUT(events);
BPF_PERF_OUTPUT(try);

struct data_t {
    u32 pid;
    char comm[TASK_COMM_LEN];
};

struct sys_enter_openat_t {
    uint64_t unused;
    u32 _nr;
    u64 dfd;
    char * filename;
    u64 flags;
    u64 mode;
};

int sys_enter_opentat_fn(struct sys_enter_openat_t *args){

    struct data_t data = {};
    u32 pid = (u32)(bpf_get_current_pid_tgid() >> 32);

    data.pid = pid;
    bpf_probe_read_str(data.comm, TASK_COMM_LEN, args->filename);
    bpf_trace_printk("openat works %d \\n", pid);

    events.perf_submit(args, &data, sizeof(data));
    data.pid = 0;
    try.perf_submit(args, &data, sizeof(data));

    return 0;
}