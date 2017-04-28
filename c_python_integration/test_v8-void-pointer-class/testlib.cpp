#include <iostream>
#include <iomanip>
#include <string>
#include <memory>
#include <Eigen/Dense>

// Include the nodebug macro to atop the asserts
#define NDEBUG
#include <assert.h>

extern "C"
{

void hello_world(){
    std::cout<< "Hello world!" << std::endl;
    std::string day = "What a beautiful day!";
    std::cout << day << std::endl;
    }

class Atoms
{
	// double * positions;
	std::unique_ptr<double []> positions;
	int nAtoms;
	const int nDim = 3;

	public:
		// Standard constructor prividing a pre-existant array
		Atoms(int nAtoms, double * positionsArray)
		{
			this->nAtoms = nAtoms;
			// This implementaition means that the Atoms.position array is not 
			// connected ot the data arrray passed ot the initialized but is a standalone object

			// this->positions = new double [nAtoms * nDim];
			this->positions = std::unique_ptr<double []>(new double[nAtoms * nDim]);
  			for (int ii = 0; ii < nAtoms * nDim; ++ii)
    			this->positions[ii] = positionsArray[ii];
		}

		//Empty constructor
		Atoms() {}

		//Destructor to free memory
		// ~Atoms() {delete[] this->positions;}

		//Dummy do-nothing function
		void do_nothing() {}

		//Simple functions to obtain nAtoms
		inline int get_nAtoms() {return this->nAtoms;}

		// Print positions to screen
		void print_positions()
		{
			std::cout<< "nAtoms: " << this->nAtoms << std::endl;
			for (int i = 0; i < nAtoms; i++)
			{
				for	(int j = 0; j < nDim; j++)
				{
					std::cout << std::setw(6) << this->positions[i * nDim + j] << "	";
				}
				std::cout << std::endl;
			}
			std::cout << std::endl;
		}

		// Set data for already defined matrix object
		void set_positions(double * positionsArray, int nAtoms)
		{
			this->nAtoms = nAtoms;
			this->positions = std::unique_ptr<double []>(new double[nAtoms * nDim]);
  			for (int ii = 0; ii < nAtoms * nDim; ++ii)
    			this->positions[ii] = positionsArray[ii];
		}
};


void initialize_Atoms_void_pointer(void ** voidAtomsPointer)
{
	//Create a new instance of Atoms by a pointer
	int numAtoms = 5;
	int numDim = 3;
	int elemN = numAtoms * numDim;
	double data_array[elemN];

	for (int i = 0; i < numAtoms; i++)
	for	(int j = 0; j < numDim; j++)
	{
		data_array[i * numDim + j] = i * numDim + j + 10;
	}
	Atoms *atoms = new Atoms(numAtoms, data_array);

	// Set the vPointer that the void pointer points to a pointer to Atoms object
	// voidAtomsPointer = static_cast<void *>(atoms);
	*voidAtomsPointer = static_cast<void *>(atoms);

	//Test call
	std::cout << std::endl << "Initializing atoms" << std::endl;
	// static_cast<Atoms *>(voidAtomsPointer)->print_positions();
	static_cast<Atoms *>(*voidAtomsPointer)->print_positions();
}

void initialize_Atoms_void_pointer_from_array(void ** voidAtomsPointer, double * data_array, int numAtoms)
{
	
	Atoms *atoms = new Atoms(numAtoms, data_array);

	// Set the vPointer that the void pointer points to a pointer to Atoms object
	//
	//WARNING
	// In This implementaition, Atoms.position array is not 
	// connected ot the data arrray passed ot the initialized but is a standalone object

	//
	*voidAtomsPointer = static_cast<void *>(atoms);

	//Test call
	std::cout << std::endl << "Initializing atoms" << std::endl;
	// static_cast<Atoms *>(voidAtomsPointer)->print_positions();
	static_cast<Atoms *>(*voidAtomsPointer)->print_positions();
}

void print_Atoms_pointer_positions(void * voidAtomsPointer)
{
	//Cast the pointer as an atoms pointer
	Atoms *atomsPointer = static_cast<Atoms *>(voidAtomsPointer);

	atomsPointer->print_positions();
}


void destroy_Atoms_void_pointer(void * voidAtomsPointer)
{
	//Cast the pointer as an atoms pointer
	Atoms *atomsPointer = static_cast<Atoms *>(voidAtomsPointer);

	//Delete it
	delete atomsPointer;
}

void testPointer(void ** testPointer)
{
	int *interVal = new int;
	*interVal=10;
	*testPointer = static_cast<void *>(interVal);
}

int main()
{
	hello_world();

	void *valPointer = NULL;
	testPointer(&valPointer);
	std::cout << *static_cast<int *>(valPointer) << std::endl;

	//Create a new instance of Atoms by a pointer
	int numAtoms = 5;
	int numDim = 3;
	int elemN = numAtoms * numDim;
	double data_array[elemN];

	for (int i = 0; i < numAtoms; i++)
	for	(int j = 0; j < numDim; j++)
	{
		data_array[i * numDim + j] = i * numDim + j;
	}
	Atoms *atoms = new Atoms(numAtoms, data_array);

	//print the atomic positions
	atoms->print_positions();

	//Create a void pointer to a pointer
	void *voidAtomsPointer;
	// Set it that the void pointer points to a pointer to Atoms object
	voidAtomsPointer = static_cast<void *>(atoms);

	// Recover the pointer to atoms object by casting the void pointer
	Atoms *atomsFromPointer = static_cast<Atoms *>(voidAtomsPointer);

	//Print positions
	atomsFromPointer->print_positions();
	//Print from a function
	print_Atoms_pointer_positions(voidAtomsPointer);

	//Use the initializer function for stufferino
	void *testVoidAtomsPointer2;

	for (int i = 0; i < numAtoms; i++)
	for	(int j = 0; j < numDim; j++)
	{
		data_array[i * numDim + j] = i * numDim + j + 10;
	}
	initialize_Atoms_void_pointer_from_array(&testVoidAtomsPointer2, data_array, numAtoms);
	print_Atoms_pointer_positions(testVoidAtomsPointer2);
	destroy_Atoms_void_pointer(testVoidAtomsPointer2);

	//Use the initializer function for stufferino
	void *testVoidAtomsPointer;

	initialize_Atoms_void_pointer(&testVoidAtomsPointer);
	print_Atoms_pointer_positions(testVoidAtomsPointer);
	destroy_Atoms_void_pointer(testVoidAtomsPointer);

	// static_cast<Atoms *>(testVoidAtomsPointer)->print_positions();
	// std::cout << static_cast<Atoms *>(testVoidAtomsPointer)->positions[0] << std::endl;

}


//End of extern C
}