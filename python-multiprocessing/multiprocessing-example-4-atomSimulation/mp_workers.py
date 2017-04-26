import os
import random
import time
import ctypes
import multiprocessing as mp

random.seed(123)

# define a example function
def rand_string(testVal, testKey="pHolder", outputQueue=None):
    """ Generates a random number and prints it"""
    os.environ['OMP_NUM_THREADS']='{:d}'.format(rank)
    os.system("echo $OMP_NUM_THREADS")
    rank = mp.current_process().name

    print "Starting ",mp.current_process().name, "with testVal: {0}".format(testVal), "with testKey: {0}".format(testKey)
    time.sleep(0.2)

    randNum = random.random()
    print "Finished with:", randNum

    #Output the result and rnk of the process that created it 
    if outputQueue is not None:
        outputQueue.put((rank, randNum))


def worker_calculate_tb_energy(numThreads, atoms=None, tb_pot=None, outputQueue=None):
    """Function to calcuate total energy with TB"""
    rank = mp.current_process().name

    # ompLib = ctypes.CDLL("libgomp.so")
    # ompLib.omp_set_num_threads(ctypes.c_int(numThreads))


    # os.system("export OMP_NUM_THREADS=3")

    # os.system("echo $OMP_NUM_THREADS")
    # os.putenv("OMP_NUM_THREADS", str(numThreads))
    # os.system("echo $OMP_NUM_THREADS")

    # database_folder="/workspace/jg2214/cnp-interface/simulations/DFTB-mio"
    # import numpy as np
    # from atomistica import TightBinding   
    # atomistica_pot = TightBinding(width=0.01,
    #     database_folder=database_folder)
    # tbEnergy = atomistica_pot.get_potential_energy(atoms)

    tbEnergy = tb_pot.get_potential_energy(atoms)

    outputQueue.put((rank, tbEnergy))