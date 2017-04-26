import random
import time
import os
import numpy as np
import multiprocessing as mp


random.seed(123)

# define a example function
def rand_string(rank, testkey="pHolder"):
    """ Generates a random number and prints it"""
    thread = rank + 1
    os.environ['OMP_NUM_THREADS']='{:d}'.format(thread)
    os.system("echo $OMP_NUM_THREADS")

    print "Starting ",mp.current_process(), "with testkey: {0}".format(testkey)
    time.sleep(0.1)

    randNum = random.random()
    print "Finished with:", randNum

    #Output the result and rnk of the process that created it 
    return (rank, randNum)