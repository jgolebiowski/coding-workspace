/* Utility functions source */
#include <stdio.h>
#include <mpi.h>

#include "UtilityFunctions.h"

/* Print hello world */
void myHelloworld()
{
    int year = 90;
    printf("Hello World from c%d!!\n", year);

}

/* Print hello world with MPI parallelism */
void hello_world_mpi(int rank, int size, char * hostname)
{
    printf("Hello World from proc %d out of %d running on %s\n", rank, size, hostname);

}