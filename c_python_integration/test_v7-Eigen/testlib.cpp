#include <iostream>
#include <iomanip>
#include <string>
#include <Eigen/Dense>

// Include the nodebug macro to atop the asserts
#define NDEBUG
#include <assert.h>

extern "C"
{

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

	public:
		// Standard constructur prividing a pre-existant array
		MyMatrix(double * data_array, int rows, int cols)
		{
			this->nrows = rows;
			this->ncols = cols;
			this->data = data_array;
		}
		//Empty constructor
		MyMatrix() {}

		//Simple functions to obtain rows and cols of the matrix
		inline int get_nrows() {return this->nrows;}
		inline int get_ncols() {return this->ncols;}

		// Overloaded bracket operator to access the values
		inline double & operator()(int i, int j) {return data[i * ncols + j];}

		// Overloaded bracket operator for constant objects:
		// V - returned reference is constant | V - "this" obj in funct is const
		inline const double & operator()(int i, int j) const {return data[i * ncols + j];}

		// Print data to screen
		void print_data()
		{
			for (int i = 0; i < nrows; i++)
			{
				for	(int j = 0; j < ncols; j++)
				{
					std::cout << std::setw(6) << (*this)(i,j) << "	";
				}
		std::cout << std::endl;
			}
		}

		// Set data for already defined matrix object
		void set_data(double * data_array, int rows, int cols)
		{
			this->nrows = rows;
			this->ncols = cols;
			this->data = data_array;
		}
};

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

void square_eMatrix(double * data_array, const int nrows, const int ncols)
{
	Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> 
														eMat(data_array, nrows, ncols);
	eMat.array() = eMat.array().square();

}

void return_eMatrix(double * dataArray, double * retArray,const int nrows, const int ncols)
{
	Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> 
														eMat(dataArray, nrows, ncols);
	Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> 
														retMat(retArray, nrows, ncols);

	retMat.array() = eMat.array().square();
}

void multiply_eMatrix(double * inputArr1, double * inputArr2, double * retArr, 
															int nrows, int ncols)
{
	assert(nrows == ncols);
	Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> 
														inputMat1(inputArr1, nrows, ncols);
	Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> 
														inputMat2(inputArr2, nrows, ncols);
	Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> 
														retMat(retArr, nrows, ncols);
	retMat = inputMat1 * inputMat2;													

}

int main()
{
	int rowsN = 1000;
	int colsN = 1000;
	int elemN = colsN * rowsN;
	double data_array[elemN];

	for (int i = 0; i < rowsN; i++)
	for	(int j = 0; j < colsN; j++)
	{
		data_array[i * colsN + j] = i + j;
	}

	int iter = 100;

	for (int k = 0; k < iter; k++)
	{
		square_matrix(data_array, rowsN, colsN);
	}

	return 0;
}


//End of extern C
}