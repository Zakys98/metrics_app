# metrics_app

System that tracks all syscalls and logs them to output.bin

## Requirements

Following dependencies must be installed on the host system

* Python3
* libelf
* libbpf-dev
    - https://github.com/libbpf/libbpf
    - sudo make install
    - sudo patchelf --set-rpath /usr/lib64 main
* llvm-strip
* linux-tools-$(uname -r)
* clang

## Build

```
sudo make
```

## Run

```
sudo ./main
```
