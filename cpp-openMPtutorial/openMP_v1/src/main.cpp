#include <iostream>
#include <UtilityFunctions.h>
#include <Complex.h>
#include <Mandelbrot.h>


int main()
{
	//print hello world and then run two functions
    std::cout << "Welcome to main" << std::endl;
    hello_world();
    hello_world_omp();

    //Test complex variables
    double testReal = 1;
    double testImag = 2;
    Complex testComplex(testReal, testImag);

    testComplex.print();
    testComplex = testComplex * testComplex;
    testComplex.print();
    testComplex = testComplex + testComplex;
    testComplex.print();
    std::cout << "length squared: " << testComplex.lengthSQ() << std::endl;

    Complex testComplexTwo(testReal, testImag);
    testComplexTwo.print();
    testComplexTwo = (testComplexTwo * testComplexTwo) + testComplexTwo;
    testComplexTwo.print();


    //Run the Mandelbrot area evaluation
    double manArea = calculateMandelbrotAreaOMP(2000, 2000);
    std::cout << "Area of the set is " << manArea << std::endl;

	return 0;
}