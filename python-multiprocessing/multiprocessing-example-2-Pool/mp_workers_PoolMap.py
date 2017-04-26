import random
import time
import os
import numpy as np
import multiprocessing as mp


random.seed(123)

# define a example function
def rand_string(argumentsDict):
    """ Generates a random number and prints it"""
    #Set up variables
    rank = argumentsDict["rank"]
    nCPU = rank + 1
    testkey = argumentsDict["testKey"]

    os.environ['OMP_NUM_THREADS']='{:d}'.format(nCPU)
    os.system("echo $OMP_NUM_THREADS")

    print "Starting ",mp.current_process().name, "with testkey: {0}".format(testkey)
    time.sleep(0.1)

    randNum = random.random()
    print "Finished with:", randNum

    #Output the result and rnk of the process that created it 
    return (rank, randNum)