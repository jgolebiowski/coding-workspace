#include <iostream>
#include <MyMatrix.h>
#include <UtilityFunctions.h>


int main()
{
	std::cout << "Hello into my new program!" << std::endl;
	int rowsN = 10;
	int colsN = 10;
	int elemN = colsN * rowsN;
	double data_array[elemN];

	for (int i = 0; i < rowsN; i++)
	for	(int j = 0; j < colsN; j++)
	{
		data_array[i * colsN + j] = i * colsN + j;
	}
	std::cout << "Created the data array" << std::endl;

	MyMatrix data_mymatrix(data_array, rowsN, colsN);
	std::cout << "Cretaed a MyMatrix instance" << std::endl;

	data_mymatrix.print_data();
	std::cout << "Printed data" << std::endl;

	square_mymatrix(data_mymatrix);	
	
	data_mymatrix.print_data();

	return 0;
}