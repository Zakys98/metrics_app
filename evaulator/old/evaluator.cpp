#include <iostream>
#include <cstring>

#include <FileReader.hpp>

int main(int argc, char **argv) {
    if (argc < 2) {
        std::cout << "Not enough arguments: Missing input filename\n";
        return 1;
    }

    FileReader fileReader{std::string(argv[1])};
    if(argc == 3 && strcmp(argv[2], "--no-data") == 0){
        fileReader.readNoData();
    } else {
        fileReader.read();
    }
    fileReader.printHistogram();
    fileReader.print();

    return 0;
}
