#pragma once

#include <fstream>
#include <unordered_map>
#include <string>

#include "syscall_enum.h"

class FileReader {

  public:
    FileReader(const std::string &filename);
    ~FileReader();
    void read();
    void print();

  private:
    std::unordered_map<uint32_t, long> map{};
    std::ifstream input{};
};