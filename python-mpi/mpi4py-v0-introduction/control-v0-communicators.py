from mpi4py import MPI

# Create an instance of communicator class - an object responsible for 
# communicating between dfferent processors. The COMM_WORLD is a static
# reference to all the processes involved
comm = MPI.COMM_WORLD

#Get the rank of a processor executing the script
rank = comm.Get_rank()

#Get the size of the group in a communicator
size = comm.Get_size()

if (rank % 2):
    print "Hello from even processor %d out of %d" % (rank, size)

if not (rank % 2):
    print "Goodbye from odd processor %d out of %d" % (rank, size)
