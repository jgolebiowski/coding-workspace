#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <UtilityFunctions.h>
#include <Eigen/Dense>
#include <Atoms.h>
#include <LJCalculator.h>
#include <Dynamics.h>


int main()
{
    //Set Eigen cores
    Eigen::setNbThreads(1);

	//print hello world and then run two functions
    hello_world();

    //Test Atoms object
    double numAtoms = 2;
    Atoms simAtoms(numAtoms);

    simAtoms.positions << 0, 0, 0,
                          1, 0, 0;

    std::cout << simAtoms.positions << std::endl << std::endl;
    std::string fileName = "testFile.xyz";
    std::remove(fileName.c_str());
    simAtoms.printAtomsXYZ("testFile.xyz");

    //Initialize LJcalculator
    double sigma = 0.5;
    double epsilon = 1e-3;
    double rCutoff = 10;

    LJCalculator lennardCalc(sigma, epsilon, rCutoff);

    double timestep = 1e-10;
    Dynamics dynamics(&simAtoms, &lennardCalc, 0.5, fileName);

    //Run MD
    int steps = 10;
    #pragma omp parallel default(shared)
    {
        for (int i = 0; i < steps; i++)
        {
            dynamics.stepOMPorphan();
    
        }
    }


    // Rerun with serial MD
    simAtoms.positions << 0, 0, 0,
                          1, 0, 0;
    simAtoms.velocities << 0, 0, 0,
                           0, 0, 0;


    std::remove(fileName.c_str());

    Dynamics dynamics2(&simAtoms, &lennardCalc, 0.5, fileName);

    steps = 10;
    //Run MD
    for (int i = 0; i < steps; i++)
    {
        dynamics2.stepOMP();

    }


	return 0;
}