#include "../include/vmlinux.h"
#include <bpf/bpf_core_read.h>
#include <bpf/bpf_helpers.h>

#include "../include/main.h"
#include "../include/syscall_structures.h"
#include "../include/syscall_enum.h"

struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 256 * 1024);
} ring_buff SEC(".maps");

SEC("tp/syscalls/sys_enter_socket")
int handle_socket(struct sys_enter_socket *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_SOCKET *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    bpf_probe_read_kernel(data->data, SYS_ENTER_SOCKET_LEN, params);
    //data->pid = BPF_CORE_READ(task, pid);
    bpf_printk("protocol: %ld <> family: %ld\n", params->protocol, params->family);
    //data->type = SYS_ENTER_SOCKET;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

/*SEC("tp/syscalls/sys_enter_socketpair")
int handle_socketpair(struct sys_enter_socketpair *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_SOCKETPAIR *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_SOCKETPAIR;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_bind")
int handle_bind(struct sys_enter_bind *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_BIND *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_BIND;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_listen")
int handle_listen(struct sys_enter_listen *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_LISTEN *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_LISTEN;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_accept4")
int handle_accept4(struct sys_enter_accept4 *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_ACCEPT4 *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_ACCEPT4;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_accept")
int handle_accept(struct sys_enter_accept *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_ACCEPT *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_ACCEPT;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_connect")
int handle_connect(struct sys_enter_connect *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_CONNECT *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    //data->pid = BPF_CORE_READ(task, pid);
    data->type = SYS_ENTER_CONNECT;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_getsockname")
int handle_getsockname(struct sys_enter_getsockname *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_GETSOCKNAME *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    //data->pid = BPF_CORE_READ(task, pid);
    data->type = SYS_ENTER_GETSOCKNAME;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_getpeername")
int handle_getpeername(struct sys_enter_getpeername *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_GETPEERNAME *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_GETPEERNAME;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_sendto")
int handle_sendto(struct sys_enter_sendto *params){
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_SENDTO *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_SENDTO;
    bpf_probe_read_kernel(data->data, SYS_ENTER_SENDTO_LEN, params);
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_recvfrom")
int handle_recvfrom(struct sys_enter_recvfrom *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_RECVFROM *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_RECVFROM;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_setsockopt")
int handle_setsockopt(struct sys_enter_setsockopt *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_SETSOCKOPT *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_SETSOCKOPT;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_getsockopt")
int handle_getsockopt(struct sys_enter_getsockopt *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_GETSOCKOPT *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_GETSOCKOPT;
    bpf_ringbuf_submit(data, 0);

    return 0;
}

SEC("tp/syscalls/sys_enter_shutdown")
int handle_shutdown(struct sys_enter_shutdown *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_SHUTDOWN *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }
    data->type = SYS_ENTER_SHUTDOWN;
    bpf_ringbuf_submit(data, 0);

    return 0;
}*/

/*SEC("tp/syscalls/sys_enter_execve")
int handle_execve(struct sys_enter_execve *params) {
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct Data *evt = {0};

    evt = bpf_ringbuf_reserve(&ring_buff, sizeof(*evt), 0);
    if (!evt) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }

    evt->pid = BPF_CORE_READ(task, pid);
    bpf_probe_read_user_str(evt->filename, sizeof(evt->filename), params->filename);
    evt->type = SYS_ENTER_OPEN_BY_HANDLE_AT;
    bpf_ringbuf_submit(evt, 0);
    //bpf_printk("Execve Called\n");

    return 0;
}

SEC("tp/syscalls/sys_enter_open")
int handle_open(struct sys_enter_open *params) {

    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct Data *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }

    data->pid = BPF_CORE_READ(task, pid);
    bpf_probe_read_user_str(data->filename, sizeof(data->filename), params->filename);
    data->type = SYS_ENTER_OPEN;
    bpf_ringbuf_submit(data, 0);
    //bpf_printk("Open Called\n");

    return 0;
}

SEC("tp/syscalls/sys_enter_openat")
int handle_openat(struct sys_enter_openat *params) {

    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    struct USER_SYS_ENTER_OPENAT *data = {0};

    data = bpf_ringbuf_reserve(&ring_buff, sizeof(*data), 0);
    if (!data) {
        bpf_printk("Ringbuffer not reserved\n");
        return 0;
    }

    data->pid = BPF_CORE_READ(task, pid);
    bpf_probe_read_user_str(data->filename, sizeof(data->filename), params->filename);
    data->type = SYS_ENTER_OPENAT;
    bpf_ringbuf_submit(data, 0);
    bpf_printk("Openat Called\n");

    return 0;
}*/

char LICENSE[] SEC("license") = "GPL";
