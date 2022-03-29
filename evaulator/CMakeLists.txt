CMAKE_MINIMUM_REQUIRED(VERSION 3.18)
PROJECT(evaulator CXX)

SET(CMAKE_CXX_STANDARD 17)

FIND_PACKAGE(Python3 REQUIRED)

FILE(GLOB_RECURSE source_files "source/*")

ADD_EXECUTABLE(${PROJECT_NAME} eval.cpp ${source_files})
TARGET_INCLUDE_DIRECTORIES(${PROJECT_NAME} PUBLIC "include/*")

ADD_CUSTOM_TARGET(
    structures ALL
    COMMAND clang ../../scripts/generator/sizer.c -o sizer
    COMMAND ./sizer > sizes
    COMMAND sudo ${PYTHON_EXECUTABLE} ../../scripts/generator/generator.py "-p" "sys_enter_*" "-n" "../include/syscall_structures.h" "--structure"
    COMMAND sudo ${PYTHON_EXECUTABLE} ../../scripts/generator/generator.py "-p" "sys_enter_*" "-n" "../include/syscall_enum.h" "--enum"
    COMMAND sudo ${PYTHON_EXECUTABLE} ../../scripts/generator/generator.py "-p" "sys_enter_*" "-n" "../include/helper.h" "--helper"
    BYPRODUCTS syscall_structures.h syscall_enum.h helper.h sizer sizes
    COMMENT "Generating syscall_structures.h syscall_enum.h helper.h"
)
#probably needed: sudo chmod +r sudo

ADD_DEPENDENCIES(${PROJECT_NAME} structures)