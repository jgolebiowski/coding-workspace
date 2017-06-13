#pragma once
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <Eigen/Dense>


//
// This class hold most of the data about the structure
// Such as atomic positions, cell as well as results from 
// The calculator
//

class Atoms
{
public:
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> positions;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> velocities;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> forces;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> cell;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> energies;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> masses;

    int nAtoms;
    double kinEne, potEne;
    static const int nDim = 3;

    //Standard constructor with num of atoms
    Atoms(double numAtoms);

    //Empty constructor just in case
    Atoms();

    //Destructor, so far not neede
    // ~Atoms();

    //Print atoms to file
    void printAtomsXYZ(std::string fileName);

    //Read atoms from file
    void readAtomsXYZ(std::string fileName);
    
};