cmake_minimum_required(VERSION 3.21.0)

project(metrics_app)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} bcc_bpf elf bcc)