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

#Define a simple trapezodal rule 
a = 0
b = 10
n = 1e8

def fXSquared(x):
    return x**6

def integrateRange(a, b, n, f):
    # Numerically integrate the trapezoid rule on the interval fom a to b

    #Take care of double counting 
    integral = -(f(a) + f(b)) / 2.0

    # n+1 endpoints ot get n trapezoids
    # The formula for each loop is 
    # int = int + f(x) * (b - a) / n
    
    for x in np.linspace(a, b, n+1):
        integral = integral + f(x)
    integral = integral * (b - a) / n
    return integral

# integral = integrateRange (a, b, n, fXSquared)
# print "With %d trapezoids we estimate the integral as %f" % (n, integral)

# Divide the work between the number of processors each gets a share of the range 
# and a share of the trapezoids

#range for each proc
localRange = float(b - a) / size

#nmber of n for each provessor
localN = int(n / size)
if rank == 0:
    print "number of steps for each proc %f" % localN
    print "Total number of steps %d" % (localN * size)

    print "range for each proc %f" % localRange
    print "Total range %f" % (localRange * size)

#local coordinants for each proc
localA = a + rank * localRange
localB = localA + localRange

#Initialize the variables, mpi4py only allows transferring numpy objects

# local integration value
localInt = np.zeros(1)
#recieve buffer for sending data
recvBuffer = np.zeros(1)

#Now each processor will perform integration on its value
localInt[0] = integrateRange(localA, localB, localN, fXSquared)

#rootTotal - the final value of integration on root
rootTotal = np.zeros(1)

#Reduce all int values by summing them and sending to the root
comm.Reduce(localInt, rootTotal, op=MPI.SUM, root=0)

#Root prints the result
if rank == 0:
    print "With %d trapezoids we estimate the integral as %f" % (n, rootTotal)
