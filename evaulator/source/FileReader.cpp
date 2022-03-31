#include <FileReader.hpp>
#include <helper.h>

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>

FileReader::FileReader(const std::string &filename) {
    input.open(filename, std::ios::binary);
}

FileReader::~FileReader() {
    input.close();
}

void FileReader::read() {
    while (!input.eof()) {
        uint32_t type;
        input.read((char *)&type, sizeof(uint32_t));
        auto it = map.find(type);
        if (it == map.end()) {
            std::pair<uint32_t, long> pair{type, 1};
            map.insert(pair);
        } else {
            map[type] = it->second + 1;
        }

        char syscall[syscallSize[type]];
        input.read((char *)&syscall, syscallSize[type]);
    }
}

static bool compareElementsInMap(std::pair<uint32_t, long> &first,
                                 std::pair<uint32_t, long> &second) {
    return first.second > second.second;
}

void FileReader::print() {
    std::vector<std::pair<uint32_t, long>> ordered{map.begin(), map.end()};
    std::sort(ordered.begin(), ordered.end(), compareElementsInMap);
    for (const std::pair<uint32_t, long> &syscall : ordered) {
        std::cout << std::setfill(' ') << std::setw(3) << syscall.first << std::setfill(' ') << std::setw(28) << syscallName[syscall.first] << std::setfill(' ') << std::setw(10) << syscall.second << "\n";
    }
}
