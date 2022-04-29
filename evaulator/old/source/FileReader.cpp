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

void FileReader::readNoData() {
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
    }
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

std::vector<std::pair<uint32_t, long>> FileReader::orderedMap() {
    std::vector<std::pair<uint32_t, long>> ordered{map.begin(), map.end()};
    std::sort(ordered.begin(), ordered.end(), compareElementsInMap);
    return ordered;
}

void FileReader::print() {
    std::vector<std::pair<uint32_t, long>> ordered = orderedMap();
    int numberOfcalls = 0;
    for (const std::pair<uint32_t, long> &syscall : ordered) {
        std::cout << std::setfill(' ') << std::setw(3) << syscall.first << std::setfill(' ') << std::setw(28) << syscallName[syscall.first] << std::setfill(' ') << std::setw(10) << syscall.second << "\n";
        numberOfcalls += syscall.second;
    }
    std::cout << "Number of system calls: " << numberOfcalls << '\n';
}

static bool underThousand(std::pair<uint32_t, long> &element) {
    return element.second < 1000 ? true : false;
}

void FileReader::printHistogram() {
    std::vector<std::pair<uint32_t, long>> histogram = orderedMap();
    histogram.erase(std::remove_if(histogram.begin(), histogram.end(), underThousand), histogram.end());
    histogram.erase(histogram.begin()); // dohodnout se s Honzou
    int largest = histogram[0].second / 1000;
    for (int i = largest; i > 0; i--) {
        for (int j = 0; j < histogram.size(); j++) {
            if (i * 1000 <= histogram[j].second)
                std::cout << " #  ";
            else
                std::cout << "    ";
        }
        std::cout << '\n';
    }
    for (int i = 0; i < histogram.size(); i++) {
        std::cout << histogram[i].first << ' ';
    }
    std::cout << '\n';
    for (int i = 0; i < histogram.size(); i++) {
        std::cout << histogram[i].first << " = " << syscallName[histogram[i].first] << '\n';
    }
}