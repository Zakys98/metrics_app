#pragma once

/**
 * @brief Logger initialize
 *
 * @param filename name of the output file
 * @return int 0 on success, otherwise 1
 */
int loggerInit(const char *filename);

/**
 * @brief Log time with type to the output file
 *
 * @param buffer data
 * @param size size of the data
 */
void loggerLogType(void *buffer, size_t size);

/**
 * @brief Log data to the output file
 *
 * @param buffer data
 * @param size size of the data
 */
void loggerLogData(void *buffer, size_t size);

/**
 * @brief Logger destroy
 *
 * Close output file
 *
 */
void loggerDestroy();