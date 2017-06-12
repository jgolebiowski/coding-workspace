#include <iostream>
#include <omp.h>
#include <Complex.h>
#include <Mandelbrot.h>


//Calculate the area of a Mandelbrot set using openMP with for loops
double calculateMandelbrotAreaForLoops(int numPoints, int maxIter)
{
    double setArea = 0;
    Complex z(0, 0);
    Complex c(0, 0);
    int numOutside = 0;

    #pragma omp parallel default(none) \
            private(c, z) shared(numPoints, maxIter) \
            reduction(+:numOutside)
    {
        //Define parallel variables
        // int size = omp_get_num_threads();
        // int rank = omp_get_thread_num();

        #pragma omp for collapse(2) schedule(static)
        for (int i = 0; i < numPoints; i++)
        for (int j = 0; j < numPoints; j++)
        {
            setInitialValue(c, i, j, numPoints);
            if (testIfOutside(c, z, maxIter))
            {
                numOutside++;
            }
        }
    }

    setArea = 2.0 * 2.5 * 1.125 *
              static_cast<double>(numPoints * numPoints - numOutside) /
              static_cast<double>(numPoints * numPoints);
    // double error = setArea / static_cast<double>(numPoints);

    return setArea;
}

//Calculate the area of a Mandelbrot set using openMP
double calculateMandelbrotAreaOMP(int numPoints, int maxIter)
{
    double setArea = 0;
    Complex z(0, 0);
    Complex c(0, 0);
    int numOutside = 0;

    // private - each process has its own version of a variable
    // They are uninitialized (random values)

    // firstprivate - each process has its own version of a variable
    // They are initialized to values before the parallel region

    // shared - processes share one variable
    // caution when modifying it 

    //V ariables initialized inside the parallel region act
    // private vars, one for each process

    #pragma omp parallel default(none) \
            private(c, z) shared(numPoints, maxIter) \
            reduction(+:numOutside)
    {
        //Define parallel variables
        int size = omp_get_num_threads();
        int rank = omp_get_thread_num();
    
        //Find the chunk for each processor
        int numPointsChunk = numPoints / size;
        //Find the inital and final point for each processor
        int startPointLocal = numPointsChunk * rank;
        int finalPointLocal = startPointLocal + numPointsChunk;

        for (int i = startPointLocal; i < finalPointLocal; i++)
        for (int j = 0; j < numPoints; j++)
        {
            setInitialValue(c, i, j, numPoints);
            if (testIfOutside(c, z, maxIter))
            {
                numOutside++;
            }
        }
    }

    setArea = 2.0 * 2.5 * 1.125 *
              static_cast<double>(numPoints * numPoints - numOutside) /
              static_cast<double>(numPoints * numPoints);
    // double error = setArea / static_cast<double>(numPoints);

    return setArea;
}


//Calculate the area of a Mandelbrot set
double calculateMandelbrotArea(int numPoints, int maxIter)
{
    double setArea;
    // double error;
    Complex z(0, 0);
    Complex c(0, 0);
    int numOutside = 0;



    for (int i = 0; i < numPoints; i++)
    for (int j = 0; j < numPoints; j++)
    {
        setInitialValue(c, i, j, numPoints);
        if (testIfOutside(c, z, maxIter))
        {
            numOutside++;
        }
    }

    setArea = 2.0 * 2.5 * 1.125 *
              static_cast<double>(numPoints * numPoints - numOutside) /
              static_cast<double>(numPoints * numPoints);
    // error = setArea / static_cast<double>(numPoints);

    return setArea;
}

//Set initial c values for the Mandelbrot calculation
void setInitialValue(Complex &c, int i, int j, int numPoints)
{
    double initReal = -2.0 + 2.5 * static_cast<double>(i) /
                          static_cast<double>(numPoints) + 1e-7;
    double initImag = 1.125 * static_cast<double>(j) /
                          static_cast<double>(numPoints) + 1e-7;

    c.set_values(initReal, initImag);
}

//test if the number c is outside the Mandelbrot set
int testIfOutside(Complex &c, Complex &z, int maxIter)
{
    double setTolerance = 4.0;
    int outsideFlag = 0;

    z = c;
    for (int iter = 0; iter < maxIter; iter++)
    {
        z = (z * z) + c;
        if (z.lengthSQ() > setTolerance)
        {
            outsideFlag = 1;
            break;
        }
    }
    return outsideFlag;
}