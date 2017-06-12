#include <iostream>
#include <omp.h>
#include <UtilityFunctions.h>
#include <vector>

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


//testi of the parallel for loop
void hello_world_parFor()
{
    std::cout<< "Welcome to hello world with OMP!" << std::endl;
    int numLoops = 3;
    std::vector<double> testVector(numLoops * numLoops, 0);

    #pragma omp parallel default(shared) \
            shared(testVector, numLoops)
    {
        //Define parallel variables
        int size = omp_get_num_threads();
        int rank = omp_get_thread_num();

        #pragma omp critical
        {
            std::cout << "hello from thread: "
                      << rank
                      << " out of "
                      << size
                      << std::endl;
        }

        //Barrier to wait for synchonization
        #pragma omp barrier

        // that a block of code is to be executed by a
        // single thread only. The first thread to reach the
        // SINGLE directive will execute the block There is a
        // synchronisation point at the end of the block: all the
        // other threads wait until block has been executed
        #pragma omp single
        {
            std::cout << "single block, executed by: "
                      << rank
                      << " out of "
                      << size
                      << std::endl;
        }

        //collapsed loop with a static schedule
        #pragma omp for collapse(2)\
                schedule(static)
        for (int i = 0; i < numLoops; i++)
        for (int j = 0; j < numLoops; j++)
        {
            testVector.at(i * numLoops + j) = (i * numLoops + j)\
                                              * 100 + rank;
        }
    }
    for (unsigned int i = 0; i < testVector.size(); i++)
    {
        std::cout << testVector.at(i) << " ";   
    }
    std::cout << std::endl;
}