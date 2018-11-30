//
// Created by Jacek Golebiowski on 28/10/2018.
//

#ifndef PROJECT_EXTENSION_PACKINGTOOLS_H
#define PROJECT_EXTENSION_PACKINGTOOLS_H

#include "Utilities.h"

/**
 * Get energy given a vector of distances.
 *
 * @param distances Distances of system atoms from a single molecule atom given as (n_sys_atoms, 1) matrix
 * @return energy for the given distances
 */
double getEnergy(const EigenMatrixXdRowMajor &distances);

/**
 * Get placement energy from atomic positions
 *
 * @param systemPositions positions of the system atoms as (n_sys_atoms, 3) matrix
 * @param moleculePositions positions of the molecule atoms as (n_mol_atoms, 3) matrix
 * @return This will be populated with the total energy
 */
double getPlacementEnergy(const Eigen::Ref <EigenMatrixXdRowMajor> systemPositions,
                          const Eigen::Ref <EigenMatrixXdRowMajor> moleculePositions);

#endif //PROJECT_EXTENSION_PACKINGTOOLS_H
