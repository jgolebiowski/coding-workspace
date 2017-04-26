import multiprocessing as mp
import numpy as np

import mp_workers_example as mpw

# Define the number of processes
nProc = 5

#Start the Queue
outputQueue = mp.Queue()

# Setup a list of processes that we want to run
processes = []
for rank in range(nProc):
	p = mp.Process(target=mpw.rand_string,
					args = (outputQueue, rank))
	processes.append(p)

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

#Extract results
results = []
for rank in range(nProc):
	results.append(outputQueue.get())

print results