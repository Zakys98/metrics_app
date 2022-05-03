CMAKE_MINIMUM_REQUIRED(VERSION 3.18)
project(evaulator)

FILE(GLOB_RECURSE source_files "library/*")
ADD_LIBRARY(${PROJECT_NAME} SHARED ${source_files})

SET(CMAKE_CXX_STANDARD 17)

SET(GENERATOR ${CMAKE_CURRENT_SOURCE_DIR}/../scripts/generator/generator.py)
SET(PATTERN "sys_enter_*")

FIND_PACKAGE(Python3 REQUIRED)

ADD_CUSTOM_TARGET(
    sizer ALL
    COMMAND cc ${CMAKE_CURRENT_SOURCE_DIR}/../scripts/generator/sizer.c -o sizer
    COMMAND ./sizer
    BYPRODUCTS sizer sizes
    COMMENT "Generating sizer"
)

ADD_CUSTOM_TARGET(
    generated ALL
    COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/library/syscall_structures.h" "--structure"
    COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/library/syscall_enum.h" "--enum"
    COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/library/helper.h" "--helper"
    COMMAND sudo ${PYTHON_EXECUTABLE} ${GENERATOR} "-p" ${PATTERN} "-n" "${CMAKE_CURRENT_SOURCE_DIR}/build/syscall_names" "--syscall_name"
    BYPRODUCTS syscall_structures.h syscall_enum.h helper.h syscall_names
    COMMENT "Generating syscall_structures.h syscall_enum.h helper.h syscall_names"
)

ADD_DEPENDENCIES(${PROJECT_NAME} generated)
ADD_DEPENDENCIES(generated sizer)