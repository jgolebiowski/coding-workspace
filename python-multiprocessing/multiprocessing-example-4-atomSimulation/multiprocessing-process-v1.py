import os
import multiprocessing as mp
import numpy as np

import mp_workers as mpw

import ase.units as units
import ase.io
from ase.atoms import Atoms

fileName = "system_optimized.xyz"
atoms = ase.io.read(fileName, format="extxyz")

########################################################################
#------ TB QM potential from Atomistica
########################################################################

database_folder="/workspace/jg2214/cnp-interface/simulations/DFTB-mio"

from atomistica import TightBinding
from atomistica import Atomistica
import atomistica.native as native
    
atomistica_pot = TightBinding(width=0.01,
        database_folder=database_folder)

print("QM potential initialized")

########################################################################
#------ Parallel evaluation
########################################################################

nProc = 2
numThreads = 2
#Set up the Queue
outputQueue = mp.Queue()

# Setup a list of processes that we want to run
processes = []
for rank in range(nProc):
	p = mp.Process(target=mpw.worker_calculate_tb_energy,
					name = rank + 1,
					args = (numThreads, ),
					kwargs = dict(atoms=atoms, 
									tb_pot=atomistica_pot, 
									outputQueue=outputQueue))
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

if (len(result) > 0):
	print result





















##############################################
############### TRAINING EXAMPLE
##############################################

nProc = 0
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

if (len(result) > 0):
	print result



