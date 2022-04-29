#pragma once

#include <fstream>
#include <unordered_map>
#include <vector>

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

    /**
     * @brief Prints histogram for most called syscalls
     *
     */
    void printHistogram();

  private:

    std::vector<std::pair<uint32_t, long>> orderedMap();

    // stores data divided by syscalls
    std::unordered_map<uint32_t, long> map{};
    // input file
    std::ifstream input{};
};