CMAKE_MINIMUM_REQUIRED(VERSION 3.18)
PROJECT(evaulator CXX)

SET(CMAKE_CXX_STANDARD 17)

SET(GENERATOR ${CMAKE_CURRENT_SOURCE_DIR}/../scripts/generator/generator.py)
SET(PATTERN "sys_enter_*")

FIND_PACKAGE(Python3 REQUIRED)

FILE(GLOB_RECURSE source_files "source/*")

ADD_EXECUTABLE(${PROJECT_NAME} evaluator.cpp ${source_files})
TARGET_INCLUDE_DIRECTORIES(${PROJECT_NAME} PUBLIC "include/")

ADD_CUSTOM_TARGET(
    sizer ALL
    COMMAND cc ${CMAKE_CURRENT_SOURCE_DIR}/../scripts/generator/sizer.c -o sizer
    COMMAND ./sizer > sizes
    BYPRODUCTS sizer sizes
    COMMENT "Generating sizer"
)

ADD_CUSTOM_TARGET(
    generated ALL
    COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/include/syscall_structures.h" "--structure"
    COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/include/syscall_enum.h" "--enum"
    COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/include/helper.h" "--helper"
    BYPRODUCTS syscall_structures.h syscall_enum.h helper.h
    COMMENT "Generating syscall_structures.h syscall_enum.h helper.h"
)

ADD_DEPENDENCIES(${PROJECT_NAME} generated)
ADD_DEPENDENCIES(generated sizer)