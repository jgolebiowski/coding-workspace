//
// Created by Jacek Golebiowski on 2019-02-11.
//

#ifndef TEST_CFFI_UTILITIES_H
#define TEST_CFFI_UTILITIES_H


/**
 * @brief Print Hello world
 */
extern "C"
void hello_world();

/**
 * @brief Print hello world with openMP parallelism
 */
extern "C"
void hello_world_omp();

#endif //TEST_CFFI_UTILITIES_H
