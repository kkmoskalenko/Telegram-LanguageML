cmake_minimum_required(VERSION 3.5 FATAL_ERROR)
project(tglang VERSION 2.0.0)

set(CMAKE_CXX_STANDARD 17)

add_library(tglang SHARED tglang.cpp
        generated/trees.generated.c)
