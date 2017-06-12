#include <iostream>
#include <omp.h>
#include <UtilityFunctions.h>

// Print hello world
void hello_world()
{
    std::cout<< "Hello World!" << std::endl;
}

// Print hello world with openMP parallelism
void hello_world_omp()
{
    std::cout<< "Welcome to hello world with OMP!" << std::endl;
    #pragma omp parallel
    {
        #pragma omp critical
        {
            std::cout<< "hello from thread: "
                     << omp_get_thread_num()
                     << " out of "
                     << omp_get_num_threads()
                     << std::endl;
        }
    }
}

/*void hello_world_omp()
{
    std::cout<< "Welcome to hello world with OMP!" << std::endl;
    #pragma omp parallel
    {
        std::cout<< "hello from thread: "
                 << omp_get_thread_num()
                 << std::endl;
    }
}*/