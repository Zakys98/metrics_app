#pragma once

#include <stddef.h>

/**
 * @brief Handler for syscalls from kernel space
 *
 * @param ctx context data
 * @param data incoming data from ring buffer
 * @param size size of incoming data
 * @return int 0 on succes
 */
int handle(void *ctx, void *data, size_t size);