#include <iostream>

extern "C" {

void hello_world(void);
double addition(double, double);

void hello_world(){
	std::cout<< "Hello world!\n";
}

double addition(double A, double B){
	return A + B;
}

}

