#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <Eigen/Dense>



class Atoms
{
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> positions;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> velocity;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> forces;
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> masses;

    int nAtoms
    int kinEne, potEne

public:
    //Standard constructor with num of atoms
    Atoms(double nAtoms);

    //Empty constructor just in case
    Atoms();

    //Destructor, so far not neede
    // ~Atoms();

    //Print atoms to file
    void printAtomsXYZ(String fileName);

    //Read atoms from file
    void readAtomsXYZ(String fileName);
    
};

// Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(nAtoms, nColumns, -1