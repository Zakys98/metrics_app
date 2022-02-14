#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>

#include "main.h"
#include "main.skel.h"

static void signalHandler() {
    printf("End");
    exit(0);
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

    printf("type: %d <> pid: %d file: %s\n", evt->type, evt->pid, evt->filename);

    return 0;
}

int main(void) {
    signal(SIGINT, signalHandler);
    bump_memlock_rlimit();

    struct main_bpf *skel = main_bpf__open();
    main_bpf__load(skel);
    main_bpf__attach(skel);

    struct ring_buffer *rb = ring_buffer__new(bpf_map__fd(skel->maps.ring_buff), handle, NULL, NULL);

    for (;;) {
        ring_buffer__poll(rb, 1000);
    }

    return 0;
}
