APP=eval
PATTERN=sys_enter_*
GENERATOR=../scripts/generator/generator.py

all: $(APP)

.PHONY: $(APP)
$(APP): eval.cpp FileReader.o
	g++ -std=c++17 -g eval.cpp FileReader.o -o $(APP)

FileReader.o: ./source/FileReader.cpp enum
	g++ -std=c++17 -g -c ./source/FileReader.cpp -o FileReader.o

.PHONY: enum
enum: sizer structures
	sudo python3 $(GENERATOR) -p $(PATTERN) -n ./include/syscall_enum.h --enum

.PHONY: structures
structures: sizer
	sudo python3 $(GENERATOR) -p $(PATTERN) -n ./include/syscall_structures.h --structure

.PHONY: sizer
sizer:
	clang ../scripts/generator/sizer.c -o sizer
	./sizer > sizes

clean:
	rm -rf $(APP) *.o sizer sizes
