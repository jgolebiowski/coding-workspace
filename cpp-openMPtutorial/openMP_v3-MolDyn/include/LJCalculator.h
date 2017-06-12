#pragma once
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <Eigen/Dense>
#include <Atoms.h>

class LJCalculator
{
    static const int nDim = 3;
    double sigma, epsilon;

public:
    //Standard constructor
    LJCalculator(double sigma, double epsilon);

    //Empty constructor just in case
    LJCalculator();

    //Destructor, so far not neede
    // ~LJCalculator();

    //Calculate forces and energies on Atoms
    void calculate(Atoms* atoms);
    
};