#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>

#include "./include/main.h"
#include "./include/main.skel.h"
#include "./include/logger.h"

static bool running = false;

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

    const struct Data *evt = data;

    if(evt->type != SYS_ENTER_SENDTO)
        printf("type: %d <> pid: %d file: %s\n", evt->type, evt->pid, evt->filename);
    else {
        const struct sys_enter_sendto_t *da = data;
        printf("SYS_ENTER_SENDTO: %d <> file: \n", da->len);
    }

    return 0;
}

int main(void) {
    signal(SIGINT, signalHandler);
    bump_memlock_rlimit();

    struct main_bpf *skel = main_bpf__open();
    main_bpf__load(skel);
    main_bpf__attach(skel);

    struct ring_buffer *rb = ring_buffer__new(bpf_map__fd(skel->maps.ring_buff), handle, NULL, NULL);

    running = true;
    while (running) {
        ring_buffer__poll(rb, 1000);
    }

    ring_buffer__free(rb);
    printf("End\n");

    return 0;
}
