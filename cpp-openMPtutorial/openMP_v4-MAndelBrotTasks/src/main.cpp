#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <UtilityFunctions.h>
#include <Mandelbrot.h>
#include <Eigen/Dense>
#include <Atoms.h>
#include <LJCalculator.h>
#include <Dynamics.h>


int main()
{
    //print hello world and then run two functions
    hello_world_parFor();

    //Test complex variables
    double testReal = 1;
    double testImag = 2;
    Complex testComplexTwo(testReal, testImag);
    testComplexTwo = (testComplexTwo * testComplexTwo) + testComplexTwo;

    //Run the Mandelbrot area evaluation
    double manArea = calculateMandelbrotAreaForLoops(2000, 2000);
    std::cout << "Area of the set is " << manArea << std::endl;


	return 0;
}