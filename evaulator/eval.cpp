#include <iostream>

#include "./include/FileReader.hpp"

int main(int argc, char **argv) {
    if (argc < 2) {
        std::cout << "Not enough arguments\n";
        return 1;
    }

    FileReader fileReader{std::string(argv[1])};
    fileReader.read();
    fileReader.print();

    return 0;
}
