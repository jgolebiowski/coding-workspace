#include <iostream>
#include <iomanip>
#include <string>


class Atoms
{
	double * positions;
	int nAtoms;

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
		// ~Atoms() {delete this->positions;}

		// Print positions to screen
		void print_positions()
		{
			std::cout<< "nAtoms: " << this->nAtoms << std::endl;
			int nDim = 3;
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


void destroy_Atoms_void_pointer(void * voidAtomsPointer)
{
	//Cast the pointer as an atoms pointer
	Atoms *atomsPointer = static_cast<Atoms *>(voidAtomsPointer);

	//Delete it
	delete atomsPointer;
}


int main()
{
	//Use the initializer function for getting a pointer
	void *testVoidAtomsPointer;

	initialize_Atoms_void_pointer(&testVoidAtomsPointer);
	print_Atoms_pointer_positions(testVoidAtomsPointer);
	destroy_Atoms_void_pointer(testVoidAtomsPointer);


}
