#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <UtilityFunctions.h>
#include <Eigen/Dense>
#include <Atoms.h>
#include <LJCalculator.h>


int main()
{
	//print hello world and then run two functions
    hello_world();

    //Test Atoms object
    double numAtoms = 5;
    Atoms simAtoms(numAtoms);

    std::cout << simAtoms.positions << std::endl;

    //Initialize LJcalculator
    int sigma = 5;
    int epsilon = 10;
    LJCalculator lennardCalc(sigma, epsilon);
    lennardCalc.calculate(&simAtoms);
    std::cout << simAtoms.forces << std::endl;


	return 0;
}