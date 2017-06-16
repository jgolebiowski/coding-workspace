import numpy as np
import os
import ase.io
import multiprocessing as mp
import multiprocess_worker_tightBinding as mpw


########################################################################
# ------ Read ASE atoms
########################################################################
fileName = "small_system.xyz"
# fileName = "system_optimized.xyz"
index = 0
atoms = ase.io.read(fileName, index=index, format="extxyz")
atoms.arrays["atomic_index"] = np.arange(len(atoms))


print("Atoms object initialized.")
########################################################################
# Stage 1 - TB QM potential from PLATO
########################################################################
from platoInterface.platoCalculator import PlatoCalculator

tightBindingPot = PlatoCalculator(platoDir="/home/jg2214/workspace/software/Plato/")

tightBindingPot.simParameters = dict(modelParams="MIO11",
                                     occupyFlag=1,
                                     occupyTolerance=1e-12,
                                     electronicTemperature=0.0175,
                                     runPeriodicSimulation=0,
                                     Monkhorst_Pack_mesh=1,
                                     useSCC=0,
                                     SCCloops=100,
                                     ETol=0.0,
                                     ResidueTol=1e-5,
                                     runSpinPolarized=0)

tightBindingPot.doCharges = True
tightBindingPot.doEigenvalues = True
tightBindingPot.printPIPE = True

atoms.set_calculator(tightBindingPot)
print("QM potential initialized")
########################################################################
# ------ Parallel evaluation
########################################################################
numThreads = 2
# Set up the Manager
mpManager = mp.Manager()
sharedList = mpManager.list(range(numThreads))

# Setup a list of processes that we want to run
processes = []
for rank in range(numThreads):
    p = mp.Process(target=mpw.workerRunTightBinding,
                   name=None,
                   args=(rank, numThreads, ),
                   kwargs=dict(atoms=atoms,
                               tightBindingPot=tightBindingPot,
                               sharedList=sharedList))
    processes.append(p)

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

print sharedList
