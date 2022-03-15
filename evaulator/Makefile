APP=eval

all: $(APP)

.PHONY: $(APP)
$(APP): eval.cpp FileReader.o
	g++ -std=c++17 -g eval.cpp FileReader.o -o $(APP)

FileReader.o: FileReader.cpp
	g++ -std=c++17 -g -c FileReader.cpp -o FileReader.o

clean:
	rm -rf $(APP) *.o
