#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <Eigen/Dense>
#include <Atoms.h>

//Standard constructor with num of atoms
Atoms::Atoms(double numAtoms)
{
    this->nAtoms = numAtoms;
    this->positions = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(this->nAtoms, this->nDim, 0);
    this->velocities = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(this->nAtoms, this->nDim, 0);
    this->forces = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(this->nAtoms, this->nDim, 0);
    this->energies = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(this->nAtoms, 1, 0);
    this->masses = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(this->nAtoms, 1, 0);
}

//Empty constructor just in case
Atoms::Atoms(){}

//Destructor, so far not neede
// ~Atoms();

//Print atoms to file
void Atoms::printAtomsXYZ(std::string fileName)
{
    std::cout << "Not implemented yet!" << std::endl;
}

//Read atoms from file
void Atoms::readAtomsXYZ(std::string fileName)
{
    std::cout << "Not implemented yet!" << std::endl;
}