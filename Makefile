APP=track
PATTERN=sys_enter_*
GENERATOR=scripts/generator/generator.py

all: $(APP) run

.PHONY: $(APP)
$(APP): skel logger.o handler.o track.c
	clang track.c logger.o handler.o -lbpf -lelf -o $(APP)

.PHONY: logger.o
logger.o: source/logger.c
	clang -c source/logger.c -o logger.o

.PHONY: handler.o
handler.o: handler
	clang -c source/handler.c -o handler.o

.PHONY: skel
skel: bpf
	bpftool gen skeleton track.bpf.o > ./include/track.skel.h

.PHONY: bpf
bpf: kernel user enum structures vmlinux
	clang -g -O3 -target bpf -c ./source/track.bpf.c -o track.bpf.o

.PHONY: vmlinux
vmlinux:
	bpftool btf dump file /sys/kernel/btf/vmlinux format c > ./include/vmlinux.h

.PHONY: handler
handler: sizer
	sudo python3 $(GENERATOR) -p $(PATTERN) -n ./source/handler.c --handler

.PHONY: kernel
kernel: sizer
	sudo python3 $(GENERATOR) -p $(PATTERN) -n ./source/track.bpf.c --bpf

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
run:
	sudo ./$(APP)

.PHONY: clean
clean:
	-rm -rf *.o ./include/*.skel.h ./include/vmlinux.h ./include/user.h ./include/syscall_structures.h ./source/handler.c ./include/syscall_enum.h ./source/track.bpf.c sizer sizes $(APP)
