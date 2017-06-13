#pragma once
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <Eigen/Dense>
#include <Atoms.h>
#include <LJCalculator.h>

//
// Time evolution of the system
//

class Dynamics
{
    static const int nDim = 3;
    Atoms * atoms;
    LJCalculator * calculator;

    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> accelerations;
    double timeStep;
    int nSteps;
    std::string trajName;

public:
    //Standard constructor
    Dynamics(Atoms *simAtoms, LJCalculator * simCalculator, double timeStepperino, std::string fileNAme);

    //Empty constructor just in case
    Dynamics();

    //Destructor, so far not neede
    // ~Dynamics();

    // Initialize dynamics
    void Initialize();

    // Perform one MD step
    void step();

    // Perform one MD step with OMP
    void stepOMP();

    //Perform a MD step with the parallel region defined previously
    void stepOMPorphan();

    //print thermo status
    void printThermoStatus();

    
};