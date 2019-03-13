//
// Created by Jacek Golebiowski on 2019-02-11.
//

#include <iostream>
#include <omp.h>
#include "utilities.h"


/**
 * @brief Print Hello world
 */
extern "C"
void hello_world()
{
    int randomNumber = 10;
    std::cout << "Helllo world! "
              << "The random number is "
              << randomNumber << std::endl;
}

/**
 * @brief Print hello world with openMP parallelism
 */
extern "C"
void hello_world_omp()
{
    std::cout << "Hello world from OMP!" << std::endl;
    #pragma omp parallel shared(std::cout) default(none)
    {
        #pragma omp critical
        {
            int rank = omp_get_thread_num();
            int size = omp_get_num_threads();
            std::cout << "Hello from thread "
                      << rank
                      << " out of "
                      << size
                      << std::endl;
        }
    }
}