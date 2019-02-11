cmake_minimum_required(VERSION 3.7)
project(project_extension)

# Gather all source files and define an executable
# Here, either compile tst/main or tst/test_main and all test cases
file(GLOB ${PROJECT_NAME}_src
        src/*.c

        tst/*.c
        )

# Build as an executable or a library
add_executable(${PROJECT_NAME} ${${PROJECT_NAME}_src})

# Add some libraries
#target_link_libraries(${PROJECT_NAME} -L/path/to/library)
#target_link_libraries(${PROJECT_NAME} -l{library_name})
target_link_libraries(${PROJECT_NAME} -L/usr/local/lib)
target_link_libraries(${PROJECT_NAME} -lgsl -liomp5 -lcblas)

# Include appropriate directories
#target_include_directories(${PROJECT_NAME} PUBLIC /path/to/include)
target_include_directories(${PROJECT_NAME} PUBLIC src)
target_include_directories(${PROJECT_NAME} PUBLIC tst)
target_include_directories(${PROJECT_NAME} PUBLIC /usr/local/include)


# Set c specifications
if(APPLE)
#    target_link_libraries(${PROJECT_NAME} -lomp)
    set(CMAKE_C_FLAGS "-Wall -Wextra -pedantic -fdiagnostics-color -Xpreprocessor -fopenmp -O0 -g")
else()
    set(CMAKE_C_COMPILER gcc)
    set(CMAKE_C_FLAGS "-Wall -Wextra -pedantic -fdiagnostics-color -fopenmp -O0 -g")
endif()

# ------ GCC options
#if(APPLE)
#    set(CMAKE_C_COMPILER gcc-8)
#else()
#    set(CMAKE_C_COMPILER gcc)
#endif()
#set(CMAKE_C_FLAGS "-Wall -Wextra -pedantic -fdiagnostics-color -Wno-cast-function-type -fopenmp -O0 -g")