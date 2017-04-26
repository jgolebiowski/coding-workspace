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
    std::string day = "What a beautiful day!";
    std::cout << day << std::endl;
    }

class Atoms
{
	double * positions;
	std::unique_ptr<double []> positions;
	int nAtoms;
	int nDim = 3;

	public:
		// Standard constructor prividing a pre-existant array
		Atoms(int nAtoms, double * positionsArray)
		{
			this->nAtoms = nAtoms;
			this->positions = positionsArray;
		}

		//Empty constructor
		Atoms() {}

		//Destructor to free memory
		// ~Atoms() {delete[] this->positions;}

		//Dummy do-nothing function
		void do_nothing() {}

		//Simple functions to obtain nAtoms
		inline int get_nAtoms() {return this->nAtoms;}

		//Modify a position
		void modify_position(int atomNumber, int dimNumber, double newPosition)
		{
			this->positions[atomNumber * nDim + dimNumber] = newPosition;
		}

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
			this->positions = positionsArray;
		}
};



void initialize_Atoms_with_positions(void ** voidAtomsPointer, double * data_array, int numAtoms)
{
	
	Atoms *atoms = new Atoms(numAtoms, data_array);

	// Set the vPointer that the void pointer points to a pointer to Atoms object
	*voidAtomsPointer = static_cast<void *>(atoms);

	//Test call
	std::cout << std::endl << "Initializing atoms" << std::endl;
	static_cast<Atoms *>(*voidAtomsPointer)->print_positions();
}

void print_Atoms_pointer_positions(void * voidAtomsPointer)
{
	//Cast the pointer as an atoms pointer
	Atoms *atomsPointer = static_cast<Atoms *>(voidAtomsPointer);

	atomsPointer->print_positions();
}

void modify_Atoms_pointer_positions(void * voidAtomsPointer, int atomNumber, int dimNumber, double newPosition)
{
	//Cast the pointer as an atoms pointer
	Atoms *atomsPointer = static_cast<Atoms *>(voidAtomsPointer);

	atomsPointer->modify_position(atomNumber, dimNumber, newPosition);
}


void destroy_Atoms_void_pointer(void * voidAtomsPointer)
{
	//Cast the pointer as an atoms pointer
	Atoms *atomsPointer = static_cast<Atoms *>(voidAtomsPointer);

	//Delete it
	delete atomsPointer;
}


int main()
{
	hello_world();


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

	//Use the initializer function for stufferino
	void *testVoidAtomsPointer;

	for (int i = 0; i < numAtoms; i++)
	for	(int j = 0; j < numDim; j++)
	{
		data_array[i * numDim + j] = i * numDim + j + 10;
	}

	initialize_Atoms_with_positions(&testVoidAtomsPointer, data_array, numAtoms);
	print_Atoms_pointer_positions(testVoidAtomsPointer);
	modify_Atoms_pointer_positions(testVoidAtomsPointer, 3, 2, 100.0);
	print_Atoms_pointer_positions(testVoidAtomsPointer);
	destroy_Atoms_void_pointer(testVoidAtomsPointer);

}


//End of extern C
}