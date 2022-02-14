APP=main

.PHONY: $(APP)
$(APP): skel
	clang main.c -lbpf -lelf -o $(APP)

.PHONY: skel
skel: bpf
	bpftool gen skeleton main.bpf.o > main.skel.h

.PHONY: bpf
bpf: vmlinux structures enum
	clang -g -O3 -target bpf -c main.bpf.c -o main.bpf.o

.PHONY: vmlinux
vmlinux:
	bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h

.PHONY: structures
structures:
	sudo python3 scripts/generator/generator.py -p sys_enter_open* -n syscall_structures --structure

.PHONY: enum
enum:
	sudo python3 scripts/generator/generator.py -p sys_enter_open* -n syscall_enum --enum

.PHONY: run
run: $(APP)
	sudo ./$(APP)

.PHONY: clean
clean:
	-rm -rf *.o *.skel.h vmlinux.h syscall_structures.h syscall_enum.h $(APP)
