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

/*int old(void *ctx, void *data, size_t size) {
    struct user_type *type = (struct user_type *)data;
    loggerLog(&type->type, sizeof(enum Types));
    if (type->type == SYS_ENTER_SOCKET) {
        printf("USER_SYS_ENTER_SOCKET: %lu, SYS_ENTER_SOCKET_LEN: %lu\n", sizeof(struct USER_SYS_ENTER_SOCKET), SYS_ENTER_SOCKET_LEN);
        char *neco = (char *)data + sizeof(enum Types);
        struct sys_enter_socket *lala = (struct sys_enter_socket *)neco;
        printf("protocol: %ld <> family: %ld\n", lala->protocol, lala->family);
        loggerLog(neco, SYS_ENTER_SOCKET_LEN);
    } else if (type->type == SYS_ENTER_BIND) {
        printf("USER_SYS_ENTER_BIND: %lu, SYS_ENTER_BIND_LEN: %lu\n", sizeof(struct USER_SYS_ENTER_BIND), SYS_ENTER_BIND_LEN);
        char *neco = (char *)data + sizeof(enum Types);
        struct sys_enter_bind *lala = (struct sys_enter_bind *)neco;
        printf("fd: %ld <> addrlen: %ld\n", lala->fd, lala->addrlen);
        loggerLog(neco, SYS_ENTER_BIND_LEN);
    }

    return 0;
}*/

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
    printf("End\n");
    loggerDestroy();

    return 0;
}
