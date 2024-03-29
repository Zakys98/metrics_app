CMAKE_MINIMUM_REQUIRED(VERSION 3.18)
PROJECT(track C)

FIND_PACKAGE(Python3 REQUIRED)

IF (NOT ${CMAKE_C_COMPILER_ID} STREQUAL "Clang")
    MESSAGE(FATAL_ERROR "Set clang as C compiler")
ENDIF()

SET(GENERATOR "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generator/generator.py")
SET(PATTERN "sys_enter_*")

OPTION(DATA_SECTION "Syscalls with their data" OFF)

FILE(GLOB_RECURSE source_files "source/*")

ADD_EXECUTABLE(${PROJECT_NAME} track.c handler.c ${source_files})
TARGET_INCLUDE_DIRECTORIES(${PROJECT_NAME} PUBLIC "include/")
TARGET_LINK_LIBRARIES(${PROJECT_NAME} PUBLIC bpf elf)

IF(DATA_SECTION)
    ADD_CUSTOM_COMMAND(
        OUTPUT handler.c
        COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "handler.c" "--handler"
        BYPRODUCTS handler.c
        COMMENT "Generating handler.c"
    )
ELSE()
    ADD_CUSTOM_COMMAND(
        OUTPUT handler.c
        COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "handler.c" "--handler_without_data"
        BYPRODUCTS handler.c
        COMMENT "Generating handler.c without data"
    )
ENDIF()

ADD_CUSTOM_TARGET(
    sizer ALL
    COMMAND cc ${CMAKE_CURRENT_SOURCE_DIR}/scripts/generator/sizer.c -o sizer
    COMMAND ./sizer
    BYPRODUCTS sizer sizes
    COMMENT "Generating sizer"
)

IF(DATA_SECTION)
    ADD_CUSTOM_TARGET(
        generated ALL
        COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/include/syscall_structures.h" "--structure"
        COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/include/syscall_enum.h" "--enum"
        COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/include/user.h" "--user"
        COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "track.bpf.c" "--bpf"
        BYPRODUCTS syscall_structures.h syscall_enum.h user.h track.bpf.c
        COMMENT "Generating syscall_structures.h syscall_enum.h user.h track.bpf.c"
    )
ELSE()
    ADD_CUSTOM_TARGET(
        generated ALL
        COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/include/syscall_structures.h" "--structure"
        COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/include/syscall_enum.h" "--enum"
        COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/include/user.h" "--user"
        COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "track.bpf.c" "--bpf_without_data"
        BYPRODUCTS syscall_structures.h syscall_enum.h user.h track.bpf.c
        COMMENT "Generating syscall_structures.h syscall_enum.h user.h track.bpf.c without data"
    )
ENDIF()

ADD_CUSTOM_TARGET(
    bpf ALL
    COMMAND bpftool btf dump file /sys/kernel/btf/vmlinux format c > ../include/vmlinux.h
    COMMAND ${CMAKE_C_COMPILER} -g -O3 -target bpf -c track.bpf.c -o track.bpf.o
    COMMAND bpftool gen skeleton track.bpf.o > ${CMAKE_CURRENT_SOURCE_DIR}/include/track.skel.h
    BYPRODUCTS vmlinux.h track.bpf.o track.skel.h
    COMMENT "Generating track.skel.h vmlinux.h"
)

ADD_DEPENDENCIES(${PROJECT_NAME} bpf)
ADD_DEPENDENCIES(bpf generated)
ADD_DEPENDENCIES(generated sizer)