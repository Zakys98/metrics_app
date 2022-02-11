#include <iostream>
#include <string>

#include <bcc/BPF.h>

struct data_t {
    pid_t pid;
    char comm[256];
};

std::string bpf_source = R"(

    BPF_PERF_OUTPUT(mmap);

    struct data_t {
        pid_t pid;
        char comm[256];
    };

    int mmap_fn(void *ctx){
        struct data_t data = {};

        data.pid = (pid_t)(bpf_get_current_pid_tgid() >> 32);
        bpf_get_current_comm(data.comm, 256);

        //bpf_probe_read_str(data.comm, TASK_COMM_LEN, args->filename);
        //bpf_trace_printk("Openat works %d \n", pid);

        mmap.perf_submit(ctx, &data, sizeof(data));

        return 0;
    }

)";

void handler(void *cookie, void *data, int size){
    auto d = static_cast<data_t*>(data);

    std::cout << d->pid << " " << d->comm << "\n";
}

int main(void){
    ebpf::BPF bpf;

    bpf.init(bpf_source);

    auto syscall = bpf.get_syscall_fnname("mmap");

    auto rc = bpf.attach_kprobe(syscall, "mmap_fn");
    if(rc.code() != 0){
        std::cout << rc.msg();
        return 1;
    }

    auto res_open_perf = bpf.open_perf_buffer("mmap", handler);
    if(res_open_perf.code() != 0){
        std::cout << res_open_perf.msg();
        return 1;
    }

    while(0 <= bpf.poll_perf_buffer("mmap")){

    }

    return 0;
}