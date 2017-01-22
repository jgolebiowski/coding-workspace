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


rootN = 15
locN = int(rootN / size) + 1

locA = np.zeros(locN)
rootA = np.zeros(rootN)
if rank == 0:
    rootA = np.linspace(0, 1, 15)
    print "Array on root with", rootN, "elements. local elems", locN
    print rootA

sendcounts = (8, 7)
displacement = (0, 8)
comm.Scatterv([rootA, sendcounts, displacement, MPI.DOUBLE], locA, root=0)
print "Local A on process", rank, locA
