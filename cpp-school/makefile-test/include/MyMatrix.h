#pragma once
#include <iostream>
#include <iomanip>
#include <assert.h>

// Include the nodebug macro to atop the asserts
// #define NDEBUG

extern "C"
{


class MyMatrix
{
	double * data;
	int nrows;
	int ncols;
	bool destroy = false;

	public:
		// Standard constructur prividing a pre-existant array
		MyMatrix(double * data_array, int rows, int cols);
		// Constructor initializing an empty array of increasing numbers
		MyMatrix(int rows, int cols);
		//Empty constructor
		MyMatrix();

		//Destructor to free memory allocated by new (if any)
		~MyMatrix();

		// Set data for already defined matrix object
		void set_data(double * data_array, int rows, int cols);

		//Simple functions to obtain rows and cols of the matrix
		int get_nrows() const;
		int get_ncols() const;

		//Obtain the underlying data
		double * get_data();

		// Overloaded bracket operator to access the values
		double & operator()(int i, int j);

		// Overloaded bracket operator for constant objects:
		// V - returned reference is constant | V - "this" obj in funct is const
		const double & operator()(int i, int j) const;

		// Print the size to screen
		void print_data();
};

} // End of extern C