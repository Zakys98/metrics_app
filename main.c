#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>

#include "./include/logger.h"
#include "./include/user.h"
#include "./include/main.skel.h"
#include "./include/syscall_structures.h"

static bool running = false;

#pragma pack(push, 1)
struct sys_enter_socket_t {
	long unusedParams;
	int __syscall_nr;
	long family;
	long type;
	long protocol;
};
#pragma pack(pop)

static void signalHandler() {
    running = false;
}

static void bump_memlock_rlimit(void) {
    struct rlimit rlim_new = {
        .rlim_cur = RLIM_INFINITY,
        .rlim_max = RLIM_INFINITY,
    };

    if (setrlimit(RLIMIT_MEMLOCK, &rlim_new)) {
        fprintf(stderr, "Failed to increase RLIMIT_MEMLOCK limit!\n");
        exit(1);
    }
}

static int handle(void *ctx, void *data, size_t size) {
    const struct user_type *evt = data;
    //printf("type: %d <> pid: %d <> data: %s\n", evt->type, evt->pid, evt->data);
    struct user_type *type = (struct user_type *)data;
    printf("type: %d\n", type->type);
    //char *neco = (char *)data + sizeof(enum Types) + sizeof(enum Types);
    //struct sys_enter_socket_t *lala = (struct sys_enter_socket_t *)neco;
    //printf("protocol: %ld <> family: %ld\n", lala->protocol, lala->family);
    //loggerLog
    return 0;
}

int main(void) {
    signal(SIGINT, signalHandler);
    bump_memlock_rlimit();

    if (loggerInit("output.log") != 0) {
        printf("Could not initialize logger\n");
        return 1;
    }

    struct main_bpf *skel = main_bpf__open();
    main_bpf__load(skel);
    main_bpf__attach(skel);

    struct ring_buffer *rb = ring_buffer__new(bpf_map__fd(skel->maps.ring_buff), handle, NULL, NULL);

    running = true;
    while (running) {
        ring_buffer__poll(rb, 1000);
    }

    ring_buffer__free(rb);
    main_bpf__destroy(skel);
    printf("End\n");
    loggerDestroy();

    return 0;
}
