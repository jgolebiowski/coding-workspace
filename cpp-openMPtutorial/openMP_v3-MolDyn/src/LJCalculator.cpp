#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <Eigen/Dense>
#include <Atoms.h>
#include <LJCalculator.h>

//Standard constructor
LJCalculator::LJCalculator(double sigma, double epsilon, double rCutoff)
{
    this->sigma = sigma;
    this->epsilon = epsilon;
    this->rCut = rCutoff;

    //Initialice OMP locks for energy and forces changes
    omp_init_lock(&energyLock);
    omp_init_lock(&forceXLock);
    omp_init_lock(&forceYLock);
    omp_init_lock(&forceZLock);
}

//Empty constructor just in case
LJCalculator::LJCalculator(){}

//Destructor, so far not neede
// ~LJCalculator();

//Calculate forces and energies on Atoms
void LJCalculator::calculate(Atoms* atoms)
{

    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> localEnergies;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> localForces;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> distances;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> distances_6;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> distances_12;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> vectors;
        
    //Matrix of distances from atom i to j's
    distances = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(atoms->nAtoms, 1, 0);
    distances_6 = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(atoms->nAtoms, 1, 0);
    distances_12 = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(atoms->nAtoms, 1, 0);
    
    // i-j displacement vectors
    vectors = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(atoms->nAtoms, atoms->nDim, 0);
    
    //Local forces and energies
    localForces = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(atoms->nAtoms, atoms->nDim, 0);
    localEnergies = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(atoms->nAtoms, 1, 0);

    #pragma omp for schedule(static)
    for (int i = 0; i < atoms->nAtoms; i++)
    {
        for (int j = 0; j < atoms->nAtoms; j++)
        {
            vectors.row(j) = atoms->positions.row(i) - atoms->positions.row(j);
            distances(j) = vectors.row(j).squaredNorm();
        }

        // Calculate sigma over distances, warning - from now on distances are sigma/r
        distances = distances.cwiseInverse();
        // Avoid explosion
        distances(i) = 0;
        distances *= sigma;

        //Calculate distances * 6 and distances * 12
        distances_6 = distances.array().pow(6);
        distances_12 = distances.array().pow(12);

        //Calculate energies
        localEnergies = 4 * epsilon * (distances_12 - distances_6);
        //TODO: not necessary here as each thread only has one, distinct i
        // However might be usefull for the future 
        omp_set_lock(&energyLock);
        atoms->energies(i) = localEnergies.sum();
        omp_unset_lock(&energyLock);


        //Calculate forces
        localForces.col(0) = (48 * epsilon * sigma * sigma * distances.array() * distances.array()) 
                            * (distances_12.array() - distances_6.array() / 2) * vectors.col(0).array();
        localForces.col(1) = (48 * epsilon * sigma * sigma * distances.array() * distances.array()) 
                            * (distances_12.array() - distances_6.array() / 2) * vectors.col(1).array();
        localForces.col(2) = (48 * epsilon * sigma * sigma * distances.array() * distances.array()) 
                            * (distances_12.array() - distances_6.array() / 2) * vectors.col(2).array();

        // Set omp locks for modyfing the variables
        // Not needed now as each process has its values of i
        // However might be usefull later 
                            
        omp_set_lock(&forceXLock);
        atoms->forces(i, 0) = localForces.col(0).sum();
        omp_unset_lock(&forceXLock);

        omp_set_lock(&forceYLock);
        atoms->forces(i, 1) = localForces.col(1).sum();
        omp_unset_lock(&forceYLock);

        omp_set_lock(&forceZLock);
        atoms->forces(i, 2) = localForces.col(2).sum();
        omp_unset_lock(&forceZLock);

        // atoms->forces(i,0) = 0;
        // atoms->forces(i,1) = 0;
        // atoms->forces(i,2) = 0;

        // for (int j = 0; j < atoms->nAtoms; j++)
        // {
        //     //distances = sigma/r
        //     atoms->forces(i, 0) += (48 * epsilon * sigma * sigma * distances(j) * distances(j)) * (distances_12(j) - distances_6(j) / 2) * vectors(j, 0);
        //     atoms->forces(i, 1) += (48 * epsilon * sigma * sigma * distances(j) * distances(j)) * (distances_12(j) - distances_6(j) / 2) * vectors(j, 1);
        //     atoms->forces(i, 2) += (48 * epsilon * sigma * sigma * distances(j) * distances(j)) * (distances_12(j) - distances_6(j) / 2) * vectors(j, 2);
        // }

        // if (i == 0)
        // {
        //     std::cout << "TEST" << std::endl
        //               << "vectors:" << std::endl
        //               << vectors << std::endl
        //               << "distances" << std::endl
        //               << distances << std::endl
        //               << "energies:" << std::endl
        //               << localEnergies << std::endl
        //               << "forces" << std::endl
        //               << atoms->forces << std::endl;
        // }
    }
}