#include <iostream>
#include <iomanip>
#include <string>
#include <vector>

// Include the nodebug macro to atop the asserts
#define NDEBUG
#include <assert.h>

void hello_world(){
    std::cout<< "Hello world!" << std::endl;
    const char * day = "day!";
    std::cout << "What a beautiful " << day << std::endl;
    }


class MyMatrix
{
	double * data;
	int nrows;
	int ncols;
	bool destroy = false;

	public:
		// Standard constructur prividing a pre-existant array
		MyMatrix(double * data_array, int rows, int cols)
		{
			this->nrows = rows;
			this->ncols = cols;
			this->data = data_array;
		}
		// Constructor initializing an empty array of zeros
		MyMatrix(int rows, int cols)
		{
			this->nrows = rows;
			this->ncols = cols;
			this->data = new double[rows * cols];
			this->destroy = true;
			for (int i = 0; i < rows; i++)
			for	(int j = 0; j < cols; j++)
			{
				data[i * cols + j] = 0.0;
			}
		}
		//Empty constructor
		MyMatrix() {}

		//Destructor to free memory allocated by new (if any)
		~MyMatrix()
		{
			if (this->destroy == true)
			{
				delete[] this->data;
			}
		}

		//Simple functions to obtain rows and cols of the matrix
		int get_nrows() {return this->nrows;}
		int get_ncols() {return this->ncols;}

		// Overloaded bracket operator to access the values
		double & operator()(int i, int j);

		// Overloaded bracket operator for constant objects:
		// V - returned reference is constant | V - "this" obj in funct is const
		const double & operator()(int i, int j) const;

		// Print the size to screen
		void print_data();
		// Set data for already defined matrix object
		void set_data(double * data_array, int rows, int cols);
};

inline double & MyMatrix::operator()(int i, int j)
{
	assert(i >= 0 && i < nrows);
	assert(j >= 0 && j < ncols);

	// return *(this->data + i * ncols + j);
	return this->data[i * ncols + j];
}
inline const double & MyMatrix::operator()(int i, int j) const
{
	assert(i >= 0 && i < nrows);
	assert(j >= 0 && j < ncols);

	return this->data[i * ncols + j];
}
void MyMatrix::print_data()
{
	for (int i = 0; i < nrows; i++)
	{
		for	(int j = 0; j < ncols; j++)
			{
				// std::cout << std::setw(6) << data[i * ncols + j] << "	";
				std::cout << std::setw(6) << (*this)(i,j) << "	";
			}
		std::cout << std::endl;
	}
}
void MyMatrix::set_data(double * data_array, int rows, int cols)
{
	this->nrows = rows;
	this->ncols = cols;
	this->data = data_array;
}

void square_matrix(double * data_array, int nrows, int ncols)
{
	MyMatrix data_matrix(data_array, nrows, ncols);
	for (int i = 0; i < nrows; i++)
	for	(int j = 0; j < ncols; j++)
	{
		data_matrix(i, j) = data_matrix(i, j) * data_matrix(i, j);
	}
}

void square_array(double * data_array, int nrows, int ncols)
{
	for (int i = 0; i < nrows; i++)
	for	(int j = 0; j < ncols; j++)
	{
		data_array[i * ncols + j] = data_array[i * ncols + j] * data_array[i * ncols + j];
	}
}

void square_mymatrix(MyMatrix & data_mymatrix, int nrows, int ncols)
{
	for (int i = 0; i < nrows; i++)
	for	(int j = 0; j < ncols; j++)
	{
		data_mymatrix(i, j) = data_mymatrix(i, j) * data_mymatrix(i, j);
	}
}

int main()
{
	int rowsN = 10000;
	int colsN = 10000;
	int elemN = colsN * rowsN;
	double data_array[elemN];

	for (int i = 0; i < rowsN; i++)
	for	(int j = 0; j < colsN; j++)
	{
		data_array[i * colsN + j] = i * colsN + j;
	}
	MyMatrix data_mymatrix(data_array, rowsN, colsN);

	int iter = 100000;
	for (int k = 0; k < iter; k++)
	{
		square_mymatrix(data_mymatrix, rowsN, colsN);
	}

	// for (int k = 0; k < iter; k++)
	// {
	// 	square_array(data_array, rowsN, colsN);
	// }


	return 0;
}