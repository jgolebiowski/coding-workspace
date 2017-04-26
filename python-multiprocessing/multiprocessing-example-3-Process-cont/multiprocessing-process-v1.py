import multiprocessing as mp
import numpy as np

import mp_workers as mpw

nProc = 4
#Set up the Queue
outputQueue = mp.Queue()

# Setup a list of processes that we want to run
processes = []
for rank in range(nProc):
	p = mp.Process(target=mpw.rand_string,
					name = rank + 1,
					args = (2*rank +1, ),
					kwargs = dict(testKey="myString", outputQueue=outputQueue))
	processes.append(p)

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

#Extract results
result = []
for rank in range(nProc):
	result.append(outputQueue.get())

print result




#takes in command-line arguments [a,b,n]
aPoint = 0.0
bPoint = 2.0
# nPoints = 10000000
nPoints = 100

#we arbitrarily define a function to integrate
def function(x):
	"""Test function, integratetion from 0 to 1 yields 1.7183"""
	return np.exp(x)

nProc = 2

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
							name = rank + 1,
							args = (aPointLocal, bPointLocal),
							kwargs = dict(n=nPointsLocal, f=function, queue=outputQueue))
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
	result += outputQueue.get()[1]

print result