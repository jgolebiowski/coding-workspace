#include <iostream>
#include <iomanip>
#include <assert.h>
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
