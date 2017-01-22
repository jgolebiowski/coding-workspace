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

#Length of a vector
n = 10

#random numbes to generate vectors
a1 = 0
a2 = 10

#Create a vector
if rank == 0:
    rootX = np.linspace(a1, a2, n)
else:
    rootX = None


if (rank == 0):
    print "The compuation starting with"
    print rootX
    print ""

#Define variables for later use
locN = np.zeros(1)

#Test two vectors for compatibility and divide the vector between processes
if rank == 0:
    if (rootX.size != n):
        print "Vector length missmatch"
        comm.Abort()
    #The script cannot handle uneven scattering for now
    if ((n % size) != 0):
        print "Uneven data division"
        comm.Abort()
    
    locN[0] = n/size
   
# Broadcast the local N variable to all processes
comm.Bcast(locN, root=0)

#Initialize numpy arrays which will store the data
locX = np.zeros(locN[0])

# Scatter vectors between all processes
comm.Scatter(rootX, locX, root=0)

print "I am processor", rank, "and I am operating on", locX, "which has", locN, "elements"
#Compute the local dot product
locX += 2
    
#Gather the results by Gather
comm.Gather(locX, rootX, root=0)

#print out the result
if (rank == 0):
    print "The computation finished with the result of"
    print rootX
