#pragma once

/**
 * @brief Logger initialize
 *
 * @param filename name of the output file
 * @return int 0 on success, otherwise 1
 */
int loggerInit(const char *filename);

void loggerLog(void *buffer, size_t size);

/**
 * @brief
 *
 */
void loggerDestroy();