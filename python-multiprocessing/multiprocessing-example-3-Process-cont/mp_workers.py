import random
import time
import os
import numpy as np
import multiprocessing as mp

random.seed(123)

# define a example function


def rand_string(testVal, testKey="pHolder", outputQueue=None):
    """ Generates a random number and prints it"""
    rank = mp.current_process().name
    os.environ['OMP_NUM_THREADS'] = '{:d}'.format(rank)
    os.system("echo $OMP_NUM_THREADS")

    print "Starting ", mp.current_process().name, "with testVal: {0}".format(testVal), "with testKey: {0}".format(testKey)
    time.sleep(0.2)

    randNum = random.random()
    print "Finished with:", randNum

    # Output the result and rnk of the process that created it
    if outputQueue is not None:
        outputQueue.put((rank, randNum))


# this is the serial version of the trapezoidal rule
# parallelization occurs by dividing the range among processes
def integrateRange(a, b, n, f):
    """Integrate a function from a to b using the trapezoidal rule
    a - beggingng of the bracket
    b - end of the bracket
    n - number of points
    f - function to integrate"""

    integral = -(f(a) + f(b)) / 2.0
    # n+1 endpoints, but n trapazoids
    for x in np.linspace(a, b, n + 1):
        integral = integral + f(x)
    integral = integral * (b - a) / n
    return integral


def integrateRangeQueue(a, b, n=100, f=None, queue=None):
    """Integrate a function from a to b using the trapezoidal rule
    queue - mp.Queue() object to store results
    a - beggingng of the bracket
    b - end of the bracket
    n - number of points
    f - function to integrate"""

    rank = mp.current_process().name
    os.environ['OMP_NUM_THREADS'] = '{:d}'.format(rank)
    os.system("echo $OMP_NUM_THREADS")

    integral = -(f(a) + f(b)) / 2.0
    # n+1 endpoints, but n trapazoids
    for x in np.linspace(a, b, n + 1):
        integral = integral + f(x)
    integral = integral * (b - a) / n
    queue.put((rank, integral))
    print "Integrating from %f to %f using %d steps and getting %f" % (a, b, n, integral)
