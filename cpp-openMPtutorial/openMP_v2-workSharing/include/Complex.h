#pragma once

class Complex
{

public:
    double real;
    double imag;

    //Standard constructor
    Complex(double realNum, double imagNum);

    //Empty constructor just in case
    Complex();

    //Destructor not needed
    //~Complex();

    //Overload multiplication operator
    Complex operator * (Complex &numberTwo);

    //Overload addition operator
    Complex operator + (Complex &numberTwo);

    //Calculate length squared
    double lengthSQ();

    //set new values
    void set_values(double realNum, double imagNum);

    //Print function
    void print();

};