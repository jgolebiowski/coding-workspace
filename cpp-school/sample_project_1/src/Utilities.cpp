#include <iostream>
#include <omp.h>
#include <Utilities.h>


/**
 * @brief Print Hello world
 */
void helloWorld()
{
	std::cout << "Helllo world!" << std::endl;
}

/**
 * @brief Print hello world with openMP parallelism
 */
void helloWorldOmp()
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