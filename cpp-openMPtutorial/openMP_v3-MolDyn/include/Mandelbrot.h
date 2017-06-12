#pragma once
#include <Complex.h>

//Calculate the area of a Mandelbrot set using openMP with for loops
double calculateMandelbrotAreaForLoops(int numPoints = 2000, 
                               int maxIter = 2000);

//Calculate the area of a Mandelbrot set using openMP
double calculateMandelbrotAreaOMP(int numPoints = 2000, 
                                  int maxIter = 2000);

//Calculate the area of a Mandelbrot set
double calculateMandelbrotArea(int numPoints = 2000, 
                               int maxIter = 2000);

//Set initial c values for the Mandelbrot calculation
void setInitialValue(Complex &c, int i, int j, int numPoints);

//test if the number c is outside the Mandelbrot set
int testIfOutside(Complex &c, Complex &z, int maxIter);
