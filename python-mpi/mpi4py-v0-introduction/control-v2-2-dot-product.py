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
n = 3e7

#random numbes to generate vectors
a1 = 0
a2 = 10

b1 = 1
b2 = 2

#Create two vectors
if rank == 0:
    rootX = np.linspace(a1, a2, n)
    rootY = np.linspace(b1, b2, n)
else:
    rootX = None
    rootY = None


#Define variables for later use
rootDot = np.zeros(1)
locN = np.zeros(1)
locDot = np.zeros(1)

#Test two vectors for compatibility and divide the vector between processes
if rank == 0:
    if (rootX.size != rootY.size) or (rootX.size != n) or (rootY.size != n):
        print "Vector length missmatch"
        comm.Abort()
    #The script cannot handle uneven scattering for now
    if ((n % size) != 0):
        print "Uneven data division"
        comm.Abort()
    
    locN = np.array([n / size])

if (rank == 0):
    print "I am processor", rank, "and I am about to broadcast", locN
    
# Broadcast the local N variable to all processes
comm.Bcast(locN, root=0)

print "I am processor", rank, "and I have recieved", locN


#Initialize numpy arrays which will store the data
locX = np.zeros(locN[0])
locY = np.zeros(locN[0])

# Scatter vectors between all processes
comm.Scatter(rootX, locX, root=0)
comm.Scatter(rootY, locY, root=0)

#Compute the local dot product
locDot = np.dot(locX, locY)

#Gather the results by reducing them
comm.Reduce(locDot, rootDot, op=MPI.SUM, root=0)

#print out the result
if (rank == 0):
    print "The computation finished with the result of %f" % rootDot[0]











