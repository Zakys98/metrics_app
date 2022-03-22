#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>

#include "./include/logger.h"
#include "./include/main.skel.h"
#include "./include/handler.h"

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

int main(void) {
    signal(SIGINT, signalHandler);
    bump_memlock_rlimit();

    if (loggerInit("output.bin") != 0) {
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
    loggerDestroy();
    printf("Catching syscalls ended\n");

    return 0;
}
