import random
import time
import os
import numpy as np

random.seed(123)

# define a example function
def rand_string(outputQueue, rank):
    """ Generates a random number and prints it"""
    thread = rank + 1
    os.environ['OMP_NUM_THREADS']='{:d}'.format(thread)
    os.system("echo $OMP_NUM_THREADS")

    print "Starting!"
    time.sleep(0.1)

    randNum = random.random()
    print "Finished with:", randNum

    #Output the result and rnk of the process that created it 
    outputQueue.put((rank, randNum))
