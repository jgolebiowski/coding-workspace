#include <iostream>
#include <iomanip>
#include <assert.h>
#include <MyMatrix.h>
#include <UtilityFunctions.h>

void hello_world()
{
	std::cout << "Helllo world!" << std::endl;
}


void square_array(double * data_array, int nrows, int ncols)
{
	for (int i = 0; i < nrows; i++)
	for	(int j = 0; j < ncols; j++)
	{
		data_array[i * ncols + j] = data_array[i * ncols + j] * data_array[i * ncols + j];
	}
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

void square_mymatrix(MyMatrix & data_mymatrix)
{
	int nrows = data_mymatrix.get_nrows();
	int ncols = data_mymatrix.get_ncols();

	for (int i = 0; i < nrows; i++)
	for	(int j = 0; j < ncols; j++)
	{
		data_mymatrix(i, j) = data_mymatrix(i, j) * data_mymatrix(i, j);
	}
}
