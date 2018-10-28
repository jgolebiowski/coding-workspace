//
// Created by Jacek Golebiowski on 28/10/2018.
//

#include <iostream>
#include "PackingTools.h"
#include "Eigen/Eigen/Dense"
#include "Utilities.h"

/**
 * Get energy given a vector of distances. The vctor is given as a (nelements, 1) matrix
 *
 * @param distances The matrix
 * @return total energy
 */
double get_energy(EigenDynamicRowMajor &distances) {
    EigenDynamicRowMajor inversemat = -distances.array();
    inversemat(0, 0) += 10;
    std::cout << "Normal array "
              << distances
              << "new array "
              << inversemat
              << std::endl;
    return 0;
}
