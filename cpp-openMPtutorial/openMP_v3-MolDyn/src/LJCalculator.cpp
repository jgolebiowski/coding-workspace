 #include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <Eigen/Dense>
#include <Atoms.h>
#include <LJCalculator.h>

//Standard constructor
LJCalculator::LJCalculator(double sigma, double epsilon)
{
    this->sigma = sigma;
    this->epsilon = epsilon;
}

//Empty constructor just in case
LJCalculator::LJCalculator(){}

//Destructor, so far not neede
// ~LJCalculator();

//Calculate forces and energies on Atoms
void LJCalculator::calculate(Atoms* atoms)
{
    for (int i = 0; i < atoms->nAtoms; i++)
    {
        atoms->forces(i,0) = i * 10 + 0;
        atoms->forces(i,1) = i * 10 + 1;
        atoms->forces(i,2) = i * 10 + 2;

        atoms->energies(i) = i * 100;
    }
}