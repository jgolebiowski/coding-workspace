#pragma once
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <Eigen/Dense>
#include <Atoms.h>


//
// Calculates properties of the system
//

class LJCalculator
{
    static const int nDim = 3;
    double sigma, epsilon, rCut;

public:
    //Standard constructor
    LJCalculator(double sigma, double epsilon, double rCutoff);

    //Empty constructor just in case
    LJCalculator();

    //Destructor, so far not neede
    // ~LJCalculator();

    //Calculate forces and energies on Atoms
    void calculate(Atoms* atoms);
    
};