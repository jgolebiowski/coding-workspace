import random
import time
import os
import numpy as np

random.seed(123)

# define a example function
def rand_string():
    """ Generates a random number and prints it"""
    print "Starting!"
    time.sleep(0.1)
    print "Finished with:", random.random()


#this is the serial version of the trapezoidal rule
#parallelization occurs by dividing the range among processes
def integrateRange(a, b, n, f):
    """Integrate a function from a to b using the trapezoidal rule
    a - beggingng of the bracket
    b - end of the bracket
    n - number of points
    f - function to integrate"""
    
    integral = -(f(a) + f(b))/2.0
    # n+1 endpoints, but n trapazoids
    for x in np.linspace(a,b,n+1):
                    integral = integral + f(x)
    integral = integral* (b-a)/n
    return integral


def integrateRangeQueue(queue, a, b, n, f):
    """Integrate a function from a to b using the trapezoidal rule
    queue - mp.Queue() object to store results
    a - beggingng of the bracket
    b - end of the bracket
    n - number of points
    f - function to integrate"""

    thread = int(a * 10) + 1
    os.environ['OMP_NUM_THREADS']='{:d}'.format(thread)
    os.system("echo $OMP_NUM_THREADS")
    
    integral = -(f(a) + f(b))/2.0
    # n+1 endpoints, but n trapazoids
    for x in np.linspace(a,b,n+1):
                    integral = integral + f(x)
    integral = integral* (b-a)/n
    queue.put(integral)
    print "Integrating from %f to %f using %d steps and getting %f" % (a, b, n, integral)