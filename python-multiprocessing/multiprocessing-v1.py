import multiprocessing as mp
import numpy as np

import mp_workers as mpw

# Setup a list of processes that we want to run
processes = []
for i in range(5):
	p = mp.Process(target=mpw.rand_string)
	processes.append(p)

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()






#takes in command-line arguments [a,b,n]
aPoint = 0.0
bPoint = 1.0
nPoints = 500000

#we arbitrarily define a function to integrate
def function(x):
	"""Test function, integratetion from 0 to 1 yields 1.7183"""
	return np.exp(x)

nProc = 4

#Start the Queue
outputQueue = mp.Queue()

#create processes
integrateProcesses = []
for rank in range(nProc):
	stepSize = (bPoint - aPoint) / nPoints
	nPointsLocal = int(nPoints / nProc)
	aPointLocal = aPoint + rank * nPointsLocal * stepSize
	bPointLocal = aPointLocal + nPointsLocal * stepSize

	intProc = mp.Process(target = mpw.integrateRangeQueue, 
						 args = (outputQueue, aPointLocal, bPointLocal, nPointsLocal, function))
	integrateProcesses.append(intProc)

#Start evaluations
for p in integrateProcesses:
	p.start()

#Join evaluations
for p in integrateProcesses:
	p.join()

#Extract results
result = 0
for rank in range(nProc):
	result += outputQueue.get()

print result