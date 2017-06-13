#include <iostream>
#include <fstream>
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

    this->cell = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(this->nDim, this->nDim, 0);
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
    //Open a file for writing
    // std::ios::trunc - If the file is opened for output operations and it 
    // already existed, its previous content is deleted and replaced by the new one.
    std::fstream myInpFile(fileName, std::ios::out | std::ios::app);
    //myInpFile.exceptions( std::ios::failbit );   
    
    myInpFile << nAtoms << std::endl
              << "XYZ simulations file" << std::endl;

    std::string element = "H";
    for (int i = 0; i < nAtoms; i++)
    {
        myInpFile << element << " "<< this->positions.row(i) << std::endl;
    }
    myInpFile.close();
}

//Read atoms from file
void Atoms::readAtomsXYZ(std::string fileName)
{
    std::cout << "Not implemented yet!" << std::endl;
}