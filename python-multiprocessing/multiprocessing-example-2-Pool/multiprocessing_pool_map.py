import multiprocessing as mp
import numpy as np

import mp_workers_PoolMap as mpw

# Define the number of processes
nProc = 5

#Have a list to gather results
resultsQueue = []

#Create a pool of workers
globalPool = mp.Pool(processes=nProc)

argumentList = []
# Setup a list of processes that we want to run
for rank in range(nProc):
    #Create the input parameters for the mp.map function
    # It works similarly to the standard map() function
    # map(function, argumensList) is an equivalent of 
    # for arg in argumentList:
    #     function(arg)

    arg = dict(rank=rank,
                testKey="myString")
    argumentList.append(arg)

#Run the pool of workers with the map function
resultsQueue = globalPool.map_async(mpw.rand_string, argumentList)


#Do not allow any more entries
globalPool.close()
#Join the processes
globalPool.join()

#Get results from the queueu
results = resultsQueue.get()
print results