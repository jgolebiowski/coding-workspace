#include <iostream>
#include <iomanip>
#include <assert.h>
#include <MyMatrix.h>

// Include the nodebug macro to atop the asserts
// #define NDEBUG

// Standard constructur prividing a pre-existant array
MyMatrix::MyMatrix(double * data_array, int rows, int cols)
{
	this->nrows = rows;
	this->ncols = cols;
	this->data = data_array;
}

// Constructor initializing an empty array of increasing numbers
MyMatrix::MyMatrix(int rows, int cols)
{
	this->nrows = rows;
	this->ncols = cols;
	this->data = new double[rows * cols];
	this->destroy = true;
	for (int i = 0; i < rows; i++)
	for	(int j = 0; j < cols; j++)
	{
		data[i * cols + j] = i * cols + j;
	}
}

//Empty constructor
MyMatrix::MyMatrix() {}

//Destructor to free memory allocated by new (if any)
MyMatrix::~MyMatrix()
{
	if (this->destroy == true)
	{
		delete[] this->data;
	}
}

// Set data for already defined matrix object
void MyMatrix::set_data(double * data_array, int rows, int cols)
{
	this->nrows = rows;
	this->ncols = cols;
	this->data = data_array;
}

//Simple functions to obtain rows and cols of the matrix
int MyMatrix::get_nrows() const {return this->nrows;}
int MyMatrix::get_ncols() const {return this->ncols;}

//Obtain the underlying data
double * MyMatrix::get_data() {return this->data;}

// Overloaded bracket operator to access the values
double & MyMatrix::operator()(int i, int j)
{
	assert(i >= 0 && i < nrows);
	assert(j >= 0 && j < ncols);

	return this->data[i * ncols + j];
}

		// Overloaded bracket operator for constant objects:
		// V - returned reference is constant | 			V - "this" obj in funct is const
const double & MyMatrix::operator()(int i, int j) const
{
	assert(i >= 0 && i < nrows);
	assert(j >= 0 && j < ncols);

	return this->data[i * ncols + j];
}

// Print the matrix to screen
void MyMatrix::print_data()
{
	for (int i = 0; i < nrows; i++)
	{
		for	(int j = 0; j < ncols; j++)
			{
				std::cout << std::setw(4) << (*this)(i,j) << "	";
			}
		std::cout << std::endl;
	}
}