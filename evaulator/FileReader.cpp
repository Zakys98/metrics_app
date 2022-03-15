#include "FileReader.hpp"

#include <cstring>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <map>

FileReader::FileReader(const std::string &filename) {
    input.open("output.bin", std::ios::binary);
}

FileReader::~FileReader() {
    input.close();
}

void FileReader::read() {
    while (!input.eof()) {
        uint32_t type;
        input.read((char *)&type, sizeof(uint32_t));
        auto it = map.find(type);
        if(it == map.end()){
            std::pair<uint32_t, long> pair{type, 1};
            map.insert(pair);
        } else {
            map[type] = it->second + 1;
        }

        char syscall[syscallSize[type]];
        input.read((char *)&syscall, syscallSize[type]);
    }
}

void FileReader::print() {
    std::map<uint32_t, long> ordered{map.begin(), map.end()};
    for (const std::pair<uint32_t, long> &syscall : ordered) {
        std::cout << std::setfill('0') << std::setw(3) << syscall.first << " " << syscall.second << "\n";
    }
}
