import os
import random
import time
import multiprocessing as mp
from platoInterface.platoCalculator import PlatoCalculator


random.seed(123)


def worker_calculate_tb_energy(rank, size, atoms=None, tightBindingPot=None, outputQueue=None):
    """Function to calcuate total energy with TB"""

    # ------ MultiProcessing library pickes all objects and
    # ------ each workr thread recieves a copy
    # Create a new calculation seed
    tightBindingPot.calculationSeed = str(int(random.random() * 1e7)) + str(rank)

    # Set OMP values for the potential
    tightBindingPot.omp_set_threads = True
    tightBindingPot.omp_num_threads = 2

    # ------ Test
    if (rank == 0):
        atoms.positions[0, 0] += 0.1
    tightBindingPot.testPAram = rank

    # ----- Calculate energies
    tbEnergy = tightBindingPot.get_potential_energy(atoms)
    outputQueue.put((rank, tbEnergy))


def workerRunTightBinding(rank, size, atoms=None, tightBindingPot=None, sharedList=None):
    """Function to calcuate total energy with TB"""

    # ------ MultiProcessing library pickes all objects and
    # ------ each workr thread recieves a copy
    # Create a new calculation seed
    tightBindingPot.calculationSeed = str(int(random.random() * 1e7)) + str(rank)

    # Set OMP values for the potential
    tightBindingPot.omp_set_threads = True
    tightBindingPot.omp_num_threads = 2

    # ------ Test
    if (rank == 0):
        atoms.positions[0, 0] += 0.1

    # ----- Run Calculations
    tightBindingPot.calculate(atoms)
    print "Finished calculations"

    sharedList[rank] = tightBindingPot.results
