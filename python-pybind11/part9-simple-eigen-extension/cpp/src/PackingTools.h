//
// Created by Jacek Golebiowski on 28/10/2018.
//

#ifndef EXAMPLE_PROJECT_CPP_PACKINGTOOLS_H
#define EXAMPLE_PROJECT_CPP_PACKINGTOOLS_H

#include "Utilities.h"

/**
 * Get energy given a vector of distances. The vctor is given as a (nelements, 1) matrix
 *
 * @param distances The matrix
 * @return total energy
 */
double get_energy(EigenDynamicRowMajor &distances);

#endif //EXAMPLE_PROJECT_CPP_PACKINGTOOLS_H
