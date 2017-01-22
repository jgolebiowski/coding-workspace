#include <iostream>

extern "C" {

void hello_world(void);
double addition(double, double);
void twod_array_pointer_2_pointer(double **, int, int);

void hello_world(){
	std::cout<< "Hello world!\n";
}

double addition(double A, double B){
	return A + B;
}

double addition_logger(double (*function)(double, double), double A, double B){
	double value = function(A, B);
	std::cout<<"Arguments from C++:  "<<A<<" "<<B<<std::endl;
	return value;	
}

void twod_array_pointer_2_pointer(double **array, int rows, int cols){
	array[1][1] = 2;
	for (int i=0; i < rows; i++){
		for (int j=0; j < cols; j++){
			std::cout<<array[i][j]<<"\t";
			}
		std::cout<<std::endl;
		}
}

void numpy_array_operation(double *array, int rows, int cols){
	for (int i=0; i<rows; i++){
		for (int j=0; j<cols; j++){
			std::cout<<array[i * cols + j]<<"\t";
			array[i*cols + j] += 1;
		}
	std::cout<<std::endl;
	}
}
}


int main(){
	double A = 2;
	double B = 3;
	double sum = addition_logger(addition, A, B);
	std::cout<<sum<<std::endl;


	int rows = 3;
	int cols = 2;

	// Create an array  as a  double pointer to a pointer
	double ** p_p_testarray;
	// Allocate p_p_testarray as a 1d array of pointers - 
	// Create a row of pointers
	p_p_testarray = new double *[rows];
	// Set each pointer in p_p_testarray to be a 1d array
	// assign a full column to each entry
	for (int i = 0; i< rows; i++){
		p_p_testarray[i] = new double [cols];
	}
	p_p_testarray[0][1] = 2;
	twod_array_pointer_2_pointer(p_p_testarray, rows, cols);

	std::cout<<std::endl;
	// Second option, create a very long single aarray
	double single_d_array[rows * cols];
	// An equivalent of calling a [i][j]
	single_d_array[0 * cols + 1] = 2;
	numpy_array_operation(single_d_array, rows, cols);

}

