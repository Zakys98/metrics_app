#pragma once

#include <stddef.h>

/**
 * @brief Handler for syscalls from kernel space
 *
 * @param ctx
 * @param data
 * @param size
 * @return int 0 on succes
 */
int handle(void *ctx, void *data, size_t size);