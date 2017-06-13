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
}

//Empty constructor just in case
LJCalculator::LJCalculator(){}

//Destructor, so far not neede
// ~LJCalculator();

//Calculate forces and energies on Atoms
void LJCalculator::calculate(Atoms* atoms)
{

    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> localEnergies;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> distances;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> distances_6;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> distances_12;

    #pragma omp for schedule(static)\
            private(localEnergies, distances, distances_6, distances_12)
    for (int i = 0; i < atoms->nAtoms; i++)
    {
        
        //Matrix of distances from atom i to j's
        distances = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(atoms->nAtoms, 1, 0);
        distances_6 = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(atoms->nAtoms, 1, 0);
        distances_12 = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(atoms->nAtoms, 1, 0);
        
        // i-j displacement vectors
        Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> vectors;
        vectors = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(atoms->nAtoms, atoms->nDim, 0);

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
        atoms->energies(i) = localEnergies.sum();

        //Calculate forces
        atoms->forces(i,0) = 0;
        atoms->forces(i,1) = 0;
        atoms->forces(i,2) = 0;

        for (int j = 0; j < atoms->nAtoms; j++)
        {
            //distances = sigma/r
            atoms->forces(i, 0) += (48 * epsilon * sigma * sigma * distances(j) * distances(j)) * (distances_12(j) - distances_6(j) / 2) * vectors(j, 0);
            atoms->forces(i, 1) += (48 * epsilon * sigma * sigma * distances(j) * distances(j)) * (distances_12(j) - distances_6(j) / 2) * vectors(j, 1);
            atoms->forces(i, 2) += (48 * epsilon * sigma * sigma * distances(j) * distances(j)) * (distances_12(j) - distances_6(j) / 2) * vectors(j, 2);
        }

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