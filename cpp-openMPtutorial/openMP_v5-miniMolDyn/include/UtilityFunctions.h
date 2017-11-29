#pragma once
#include <Atoms.h>
#include <string>

// Initialize an atoms object from a xyz file
Atoms initializeAtomsFromXYZ(std::string fileName);

/*Print hello world*/
void hello_world();

/*Print hello world with openMP parallelism*/
void hello_world_omp();

//Print hello world with openMP parallel for loop
void hello_world_parFor();