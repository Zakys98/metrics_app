# metrics_app

System, which tracks system and detects, if operating system and hardware is able to run all
applications, we need. With this feature compute units can be swapped or system can be updated
without worrying about performance and enviroment stability.

## Requirements for track app

Following dependencies must be installed on the host system

* Python3
* libelf
* libbpf-dev
    - https://github.com/libbpf/libbpf
    - sudo make install
* llvm-strip
* linux-tools-$(uname -r)
* clang
* cmake

Minimum supported kernel version: 4.1

Kernel config option that must be enabled:

```
CONFIG_DEBUG_INFO_BTF=y
```

You need to find config and then use folowwing command to see if your kernel was build with that option.

```
grep BTF .config
```

## Requirements for evaluator app

Following dependencies must be installed on the host system

* Python3
* python3-tk
* matplotlib for Python3

## Directory structure

* evaluator - directory with evaluator app
* include - header files of track app
* source - source files of track app
* scripts - helper scripts
* scripts/generator - script that generates files needed for compilation

## Build track app

```
mkdir build
cd build
cmake .. -DCMAKE_C_COMPILER=clang
make
```

### Cmake options

PATTERN - pattern where generator search for syscall format file, defaul = tsys_enter_*

DATA_SECTION - build app and catch syscalls with their data, otherwise catch only thir types, default = OFF

## Build evaluator library

```
mkdir build
cd build
cmake ..
make
```

## Run track app

Track:
```
sudo ./track
```
If it does not work, try to use this command and then run it again:
```
sudo patchelf --set-rpath /usr/lib64 track
```

## Run evaluator app

Evaluator:
```
python3 evaluator.py -n ../build/output.bin --no-data --count --graph --hist
```

### Options

* count     - count all syscalls and print
* graph     - show diferencial graph
* hist      - show histogram
* called    - print how many times were all syscalls called
* input     - name of the input file, mandatory

One of these two has to be selected:
* data      - parses syscalls with their data
* no-data   - parses syscalls without their data
