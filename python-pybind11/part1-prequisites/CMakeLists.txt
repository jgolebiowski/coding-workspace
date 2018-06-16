cmake_minimum_required(VERSION 3.10)
project(part1_intro)

# Include pybinding
add_subdirectory(cpp/pybind11)

# Gather all source files and define an executable
file(GLOB part1_intro_src
        cpp/src/*.cpp)

# Build as an executable or a library
#add_executable(part1_intro ${part1_intro_src})
add_library(part1_intro SHARED ${part1_intro_src})
#pybind11_add_module(part1_intro SHARED ${part1_intro_src})


# Add some libraries
#target_link_libraries(part1_intro -L/usr/lib)
#target_link_libraries(part1_intro -lm)

# Include appropriate directories
target_include_directories(part1_intro PUBLIC cpp/src)
target_include_directories(part1_intro PUBLIC /Users/golejace/Documents/eigen-git-mirror)


# Set cpp specifications
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_COMPILER g++-8)
set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -Wextra -pedantic -O3 -fopenmp -fdiagnostics-color")

# Move binaries to a specified location
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY /Users/golejace/Documents/coding-workspace/python-pybind11/part1-prequisites/part1/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY /Users/golejace/Documents/coding-workspace/python-pybind11/part1-prequisites/part1/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY /Users/golejace/Documents/coding-workspace/python-pybind11/part1-prequisites/part1/lib)

set(EXECUTABLE_OUTPUT_PATH /Users/golejace/Documents/coding-workspace/python-pybind11/part1-prequisites/part1/lib)
set(LIBRARY_OUTPUT_PATH /Users/golejace/Documents/coding-workspace/python-pybind11/part1-prequisites/part1/lib)