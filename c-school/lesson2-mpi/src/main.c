/* Hello World program */
#include <stdio.h>
#include <mpi.h>

#include "UtilityFunctions.h"


int main(int argc, char **argv)
{
    int ierr, rank, size;
    char hostname[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Comm comm;
    
    ierr = MPI_Init(&argc, &argv);
    comm = MPI_COMM_WORLD;
    ierr = MPI_Comm_rank(comm, &rank);
    ierr = MPI_Comm_size(comm, &size);
    ierr = MPI_Get_processor_name(hostname, &name_len);

    hello_world_mpi(rank, size, hostname);
         
    ierr = MPI_Finalize();
    return ierr;

}