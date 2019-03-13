cmake_minimum_required(VERSION 3.7)
project(project_extension)

# Gather all source files and define an executable
# Here, either compile tst/main or tst/test_main and all test cases
file(GLOB ${PROJECT_NAME}_src
        src/*.cpp
        tst/*.cpp
        )

# Build as an executable or a library
add_executable(${PROJECT_NAME} ${${PROJECT_NAME}_src})

# Add some libraries
#target_link_libraries(${PROJECT_NAME} -L/path/to/library)
#target_link_libraries(${PROJECT_NAME} -l{library_name})
target_link_libraries(${PROJECT_NAME} -L/usr/local/lib)

# Include appropriate directories
#target_include_directories(${PROJECT_NAME} PUBLIC /path/to/include)
target_include_directories(${PROJECT_NAME} PUBLIC src)
target_include_directories(${PROJECT_NAME} PUBLIC tst)
target_include_directories(${PROJECT_NAME} PUBLIC dependencies)
target_include_directories(${PROJECT_NAME} PUBLIC /usr/local/include)


# Set cpp specifications
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -Wextra -fdiagnostics-color -fopenmp -O0 -g")

if(APPLE)
    set(CMAKE_CXX_COMPILER g++-8)
else()
    set(CMAKE_CXX_COMPILER g++)
endif()
