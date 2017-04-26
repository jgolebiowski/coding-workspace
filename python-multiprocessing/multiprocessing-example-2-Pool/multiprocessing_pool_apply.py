import multiprocessing as mp
import numpy as np

import mp_workers as mpw

# Define the number of processes
nProc = 5

#Have a list to gather results
resultsQueue = []

#Create a pool of workers
globalPool = mp.Pool(processes=nProc)

# Setup a list of processes that we want to run
for rank in range(nProc):

    #Apply the function asyncronously
    # The apply function follows the standad apply func
    # apply(function, args[, keywords]) is equivalent to function(*args, **keywords).
    # Where:
    # args: list/tuple containing arguments
    # keywords: dictionary where keys are strings
    # i.e. apply(func, [1, 2], {"key": 10, "key2": 20})


    localResult = globalPool.apply_async(mpw.rand_string,
                                    [rank],
                                    dict(testkey="myString"))
    resultsQueue.append(localResult)

#Do not allow any more entries
globalPool.close()
#Join the processes
globalPool.join()

#Get results from the queueu
results = [item.get() for item in resultsQueue]
print results