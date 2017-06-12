#include <iostream>
#include <omp.h>
#include <Complex.h>

//Standard constructor
Complex::Complex(double realNum, double imagNum)
{
    this->real = realNum;
    this->imag = imagNum;
}

//Empty contructor
Complex::Complex() {}

//Overloaded multiplication operator
Complex Complex::operator * (Complex &numberTwo)
{
    Complex finalComplex(this->real * numberTwo.real - this->imag * numberTwo.imag, 
                         this->real * numberTwo.imag + this->imag * numberTwo.real);
    return finalComplex;
}

//Overloaded addition operator
Complex Complex::operator + (Complex &numberTwo)
{
    Complex finalComplex(this->real + numberTwo.real, 
                         this->imag + numberTwo.imag);
    return finalComplex;
}

//Calculate length squared
double Complex::lengthSQ()
{
    return this->real * this->real + this->imag * this->imag;
}

//set new values
void Complex::set_values(double realNum, double imagNum)
{
    this->real = realNum;
    this->imag = imagNum;
}

//Print function
void Complex::print()
{
    std::cout << "(" << this->real << ", " 
              << this->imag << ")" << std::endl;
/*    std::cout << "Real: "
              << this->real
              << " Imag: "
              << this->imag
              << std::endl;*/
}

