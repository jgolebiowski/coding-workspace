import numpy as np
from mpi4py import MPI

# Create an instance of communicator class - an object responsible for 
# communicating between dfferent processors. The COMM_WORLD is a static
# reference to all the processes involved
comm = MPI.COMM_WORLD

#Get the rank of a processor executing the script
rank = comm.Get_rank()

#Get the size of the group in a communicator
size = comm.Get_size()

randNum = np.zeros(1)

# Have the process with rank 1 send a random number to rank 0
if rank == 1:
    randNum = np.random.random_sample(1)
    print "Process %d out of %d drew a number %f" % (rank, size, randNum[0])
    
    #Send the number to process 0
    comm.Send(randNum, dest=0)
    comm.Send(randNum, dest=2)

# Have a master process 0 recieve the random number from proc 1
if rank == 0:
    print "Process %d out of %d initially had a number %f" % (rank, size, randNum[0])

    #Revieve a number
    comm.Recv(randNum, source=1)
    print "Process %d out of %d recieved a number %f" % (rank, size, randNum[0])
    
# Have a master process 0 recieve the random number from any source
if rank == 2:
    print "Process %d out of %d initially had a number %f" % (rank, size, randNum[0])

    #Revieve a number
    comm.Recv(randNum, source=MPI.ANY_SOURCE)
    print "Process %d out of %d recieved a number %f" % (rank, size, randNum[0])
