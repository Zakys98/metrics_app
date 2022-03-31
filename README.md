# metrics_app

System, which tracks system and detects, if operating system and hardware is able to run all
applications, we need. With this feature compute units can be swapped or system can be updated
without worrying about performance and enviroment stability.

## Requirements

Following dependencies must be installed on the host system

* Python3
* libelf
* libbpf-dev
    - https://github.com/libbpf/libbpf
    - sudo make install
    - sudo patchelf --set-rpath /usr/lib64 track
* llvm-strip
* linux-tools-$(uname -r)
* clang
* cmake

Minimum supported kernel version: 4.1

Kernel config options that must be enabled:

```
CONFIG_BPF=y
CONFIG_BPF_SYSCALL=y
CONFIG_NET_CLS_BPF=m
CONFIG_NET_ACT_BPF=m
CONFIG_BPF_JIT=y
# [for Linux kernel versions 4.1 through 4.6]
CONFIG_HAVE_BPF_JIT=y
# [for Linux kernel versions 4.7 and later]
CONFIG_HAVE_EBPF_JIT=y
CONFIG_BPF_EVENTS=y
CONFIG_IKHEADERS=y
```

## Directory structure

* documentation - everything you need to know about this app
* evaulator - directory with evaulator app
* include - header files of track app
* source - source files of track app
* scripts - helper scripts
* scripts/generator - script that generates files needed for compilation

## Build

Track:
```
mkdir build
cd build
cmake .. -DCMAKE_C_COMPILER=clang
make
```
Evaulator:
```
mkdir build
cd build
cmake ..
make
```

If it does not work, try to use this command first: sudo chmod +r sudo

## Run

Track:
```
sudo ./track
```
Evaulator:
```
./evaulator <filename>
```
