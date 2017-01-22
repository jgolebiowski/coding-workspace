#include <iostream>

extern "C" {

void hello_world(void);
int return_int(int);
void call_speed(double *, int);
double cube(double);
void one_d_array(double *, int);

void hello_world(){
	std::cout<< "Hello world!\n";
}

int return_int(int param){
    return param;
}

void call_speed(double * array, int param){
}

double cube(double A){
	return A*A*A;
}

void one_d_array(double * array, int rows){
    for (int i=0; i<rows; i++){
        array[i] = cube(array[i]);
        }    
}
}


int main(){
	double A = 2;
    std::cout<<"The cube for a number:"<<A<<" is "<<cube(A)<<std::endl;


	int rows = 3;



	// Second option, create a very long single aarray
	double single_d_array[rows];
	// An equivalent of calling a [i][j]
	single_d_array[0] = 2;
	single_d_array[1] = 3;
	single_d_array[2] = 4;

    one_d_array(single_d_array, rows);
    
    for (int i=0; i<rows; i++){
        std::cout<<single_d_array[i]<<std::endl;
    }

}

