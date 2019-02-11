//
// Created by Jacek Golebiowski on 2019-02-11.
//

#include "utilities.h"

#include <omp.h>
#include <stdio.h>


/* Print hello world */
void hello_world() {
    int randomNumber = 10;
    printf("Hello, World! %d\n", randomNumber);
}

/* Print hello world with openMP parallelism */
void hello_world_omp() {
    printf("Hello world form OMP!\n");
#pragma omp parallel default(none)
    {
#pragma omp critical
        {
            int rank = omp_get_thread_num();
            int size = omp_get_num_threads();
            printf("Hello from thread %d out of %d\n", rank, size);
        }
    }
}
