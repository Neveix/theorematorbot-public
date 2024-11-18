cmake_minimum_required(VERSION 3.10)

set(CMAKE_BUILD_PARALLEL_LEVEL 0)

project(theorematorbot LANGUAGES CXX)

find_package(Boost REQUIRED)
find_package(GTest REQUIRED)

set(CMAKE_CXX_STANDARD 20)

add_compile_options(-Wall -Wextra -O2)

add_subdirectory(libs/engine)
