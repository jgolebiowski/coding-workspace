/* Utility functions source */
#include <stdio.h>
#include <omp.h>

#include "UtilityFunctions.h"

/* Print hello world */
void myHelloworld()
{
    int year = 90;
    printf("Hello World from c%d!!\n", year);

}

/* Print hello world with openMP parallelism */
void hello_world_omp()
{
    printf("Welcome to hello world with OMP!\n");
    #pragma omp parallel default(none)
    {
        #pragma omp critical
        {
            printf("Hello from thread %d out of %d\n", 
                   omp_get_thread_num(),
                   omp_get_num_threads());
        }
    }
}