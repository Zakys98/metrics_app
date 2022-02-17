APP=main
PATTERN=sys_enter_*

.PHONY: $(APP)
$(APP): skel
	clang main.c -lbpf -lelf -o $(APP)

.PHONY: skel
skel: bpf
	bpftool gen skeleton main.bpf.o > ./include/main.skel.h

.PHONY: bpf
bpf: vmlinux structures enum
	clang -g -O3 -target bpf -c ./source/main.bpf.c -o main.bpf.o

.PHONY: vmlinux
vmlinux:
	bpftool btf dump file /sys/kernel/btf/vmlinux format c > ./include/vmlinux.h

.PHONY: structures
structures: sizer
	sudo python3 scripts/generator/generator.py -p $(PATTERN) -n syscall_structures --structure
	mv -f syscall_structures.h ./include/

.PHONY: enum
enum:
	sudo python3 scripts/generator/generator.py -p $(PATTERN) -n syscall_enum --enum
	mv -f syscall_enum.h ./include/

.PHONY: sizer
sizer:
	clang scripts/generator/sizer.c -o sizer
	./sizer > sizes

.PHONY: run
run: $(APP)
	sudo ./$(APP)

.PHONY: clean
clean:
	-rm -rf *.o ./include/*.skel.h ./include/vmlinux.h ./include/syscall_structures.h ./include/syscall_enum.h sizer sizes $(APP)
