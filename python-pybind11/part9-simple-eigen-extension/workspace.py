"""Main file for the problem"""
import numba
import numpy as np
import time
from example_project.clib import example_project_cpp

@numba.jit([
    numba.float64(numba.float64[:]),
    numba.float32(numba.float32[:])
], nopython=True)
def _get_energy(distances: np.ndarray) -> float:
    """
    Calculate energy given interatomic distances

    :param distances: 1d array with distances

    :return: total energy
    """
    return np.sum(np.exp(-distances)).item()

@numba.jit([
    numba.float64(numba.float64[:, :], numba.float64[:, :]),
    numba.float32(numba.float32[:, :], numba.float32[:, :])
], nopython=True, parallel=True)
def _get_placement_energy(system_pos: np.ndarray, mol_pos: np.ndarray) -> float:
    """
    Get placement energy from atomic positions

    :param system_pos: positions of the system atoms
    :param mol_pos: positions of the molecule atoms

    :return: energy penalty
    """
    n_mol_atoms = mol_pos.shape[0]

    energy = 0
    for idx in numba.prange(n_mol_atoms):
        displacements = system_pos - mol_pos[idx, :]
        distances = np.sqrt(np.sum(np.square(displacements), axis=1))
        energy += _get_energy(distances)
    return energy


def main():
    example_project_cpp.hello_world_omp()
    N = 100

    system = np.random.uniform(low=0, high=1, size=(N, 3))
    molecule = np.random.uniform(low=0, high=1, size=(N // 10, 3))

    started_at = time.time()
    energy = _get_placement_energy(system, molecule)
    time_taken = time.time() - started_at
    print(energy)


if (__name__ == "__main__"):
    main()
