APP=main
PATTERN=sys_enter_*
GENERATOR=scripts/generator/generator.py

.PHONY: $(APP)
$(APP): skel logger.o handler.o main.c
	clang main.c logger.o handler.o -lbpf -lelf -o $(APP)

.PHONY: logger.o
logger.o: source/logger.c
	clang -c source/logger.c -o logger.o

.PHONY: handler.o
handler.o: source/handler.c handler
	clang -c source/handler.c -o handler.o

.PHONY: skel
skel: bpf
	bpftool gen skeleton main.bpf.o > ./include/main.skel.h

.PHONY: bpf
bpf: kernel user enum structures vmlinux
	clang -g -O3 -target bpf -c ./source/main.bpf.c -o main.bpf.o

.PHONY: vmlinux
vmlinux:
	bpftool btf dump file /sys/kernel/btf/vmlinux format c > ./include/vmlinux.h

.PHONY: handler
handler: sizer
	sudo python3 $(GENERATOR) -p $(PATTERN) -n ./source/handler.c --handler

.PHONY: kernel
kernel: sizer
	sudo python3 $(GENERATOR) -p $(PATTERN) -n ./source/main.bpf.c --bpf

.PHONY: user
user: sizer
	sudo python3 $(GENERATOR) -p $(PATTERN) -n ./include/user.h --user

.PHONY: enum
enum: sizer
	sudo python3 $(GENERATOR) -p $(PATTERN) -n ./include/syscall_enum.h --enum

.PHONY: structures
structures: sizer
	sudo python3 $(GENERATOR) -p $(PATTERN) -n ./include/syscall_structures.h --structure

.PHONY: sizer
sizer:
	clang scripts/generator/sizer.c -o sizer
	./sizer > sizes

.PHONY: run
run: $(APP)
	sudo ./$(APP)

.PHONY: clean
clean:
	-rm -rf *.o ./include/*.skel.h ./include/vmlinux.h ./include/user.h ./include/syscall_structures.h ./include/syscall_enum.h ./source/main.bpf.c sizer sizes $(APP)
