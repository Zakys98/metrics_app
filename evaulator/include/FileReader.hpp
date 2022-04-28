#pragma once

#include <fstream>
#include <unordered_map>

class FileReader {

  public:
    FileReader(const std::string &filename);
    ~FileReader();

    /**
     * @brief Reads input file and stores data
     *
     */
    void readNoData();

    /**
     * @brief Reads input file and stores data
     *
     */
    void read();

    /**
     * @brief Prints formatted data
     *
     */
    void print();

  private:

    // stores data divided by syscalls
    std::unordered_map<uint32_t, long> map{};
    // input file
    std::ifstream input{};
};