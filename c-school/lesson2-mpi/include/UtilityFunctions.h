/* Utility functions headers */
#pragma once
#include <stdio.h>
#include <mpi.h>

/* Print hello world */
void myHelloworld();

/* Print hello world with MPI parallelism */
void hello_world_mpi(int rank, int size, char * hostname);