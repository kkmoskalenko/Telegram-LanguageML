cmake_minimum_required(VERSION 3.5 FATAL_ERROR)
project(tglang VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)

add_library(tglang SHARED tglang.cpp vectorizer.cpp)
add_executable(tglang-tester tglang-tester.c)
add_executable(tglang-trainer tglang-trainer.cpp)

target_link_libraries(tglang-tester PRIVATE tglang)
target_link_libraries(tglang-trainer PRIVATE tglang)

if (NOT WIN32)
    target_link_libraries(tglang-tester PRIVATE m)
    if (UNIX AND NOT APPLE)
        target_link_libraries(tglang-tester PRIVATE rt)
    endif ()
else ()
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
endif ()

