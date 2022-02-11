CC=gcc
CPP=g++

LIBS=-lbcc_bpf -lelf -lbcc

main: main.cpp
	$(CPP) $(CPP_FLAGS) -o $@ $^ $(LIBS)

.PHONY: clean
clean:
	rm -rf main *.o
