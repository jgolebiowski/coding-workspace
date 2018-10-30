//
// Created by Jacek Golebiowski on 28/10/2018.
//

#include <iostream>
#include "PackingTools.h"
#include "Eigen/Dense"
#include "Utilities.h"

/**
 * Get energy given a vector of distances.
 *
 * @param distances Distances of system atoms from a single molecule atom given as (n_sys_atoms, 1) matrix
 * @return energy for the given distances
 */
double getEnergy(const EigenMatrixXdRowMajor &distances)
{
    return (-distances).array().exp().sum();
}

/**
 * Get placement energy from atomic positions
 *
 * @param systemPositions positions of the system atoms as (n_sys_atoms, 3) matrix
 * @param moleculePositions positions of the molecule atoms as (n_mol_atoms, 3) matrix
 * @return This will be populated with the total energy
 */
double getPlacementEnergy(const Eigen::Ref<EigenMatrixXdRowMajor> systemPositions,
                        const Eigen::Ref<EigenMatrixXdRowMajor> moleculePositions)
{
    long numSystemAtoms = systemPositions.rows();
    long numMoleculeAtoms = moleculePositions.rows();
    long numDims = 3;
    double totalEnergy = 0;

    EigenMatrixXdRowMajor displacements(numSystemAtoms, numDims);
    EigenMatrixXdRowMajor distances(numSystemAtoms, 1);

// const references are always shared, OPM doesnt like to be told that explicitly
#pragma omp parallel for reduction(+:totalEnergy) shared(numMoleculeAtoms) private(displacements, distances) default(none)
    for (int idx = 0; idx < numMoleculeAtoms; ++idx)
    {
        displacements = systemPositions.rowwise() - moleculePositions.row(idx);
        distances = displacements.rowwise().norm();
        totalEnergy += getEnergy(distances);
    }
    return totalEnergy;
}