#include "./include/FileReader.hpp"

int main(int argc, char **argv){
	FileReader fileReader{std::string("../output.bin")};
    fileReader.read();
    fileReader.print();
	return 0;
}
