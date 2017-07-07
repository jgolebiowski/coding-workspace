#include <iostream>
#include <iomanip>
#include <string>
#include <memory>
#include <Eigen/Dense>

#include <typeinfo>

extern "C"
{

void hello_world(){
    std::cout<< "Hello world!" << std::endl;
    std::string day = "What a beautiful day!";
    std::cout << day << std::endl;
    }

double * testFunct(){
	const int nRows = 10;
	const int nCols = 5;

	Eigen::Matrix< double, nRows, nCols, Eigen::RowMajor> testMat = Eigen::Matrix< double, nRows, nCols, Eigen::RowMajor>::Random();
	std::cout << testMat <<std::endl;
	return testMat.data();
}

class Atoms
{
	Eigen::Map< Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > positions;
	Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> neighbourList;
	double * positionsPointer;
	int nAtoms;
	static const int nDim = 3;

	public:
		// Standard constructor prividing a pre-existant array
		// Adressing positions in initializaton list is necessary since Map< Matrix<xxx> >
		// Does not have an empty constructor, only a (NULL, dim1, dim2) one
		Atoms(int nAtoms, double * positionsArray):
					positions (NULL, 0, 0),
					nAtoms (nAtoms)
		{
			// this->nAtoms = nAtoms;
			this->positionsPointer = positionsArray;

			// Despite appearances, this does not invoke the memory allocator, 
			// because the syntax specifies the location for storing the result.
			new (&(this->positions)) Eigen::Map< Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > 
														(positionsArray, nAtoms, nDim);
		}

		//Empty constructor
		Atoms():
			positions(NULL, 0, 0) 
			{}

		//Destructor to free memory
		// ~Atoms() {delete[] this->positions;}

		//Dummy do-nothing function
		void do_nothing() {}

		//Simple functions to obtain nAtoms
		inline int get_nAtoms() {return this->nAtoms;}

		//Modify a position
		void modify_position(int atomNumber, int dimNumber, double newPosition)
		{
			this->positions(atomNumber,dimNumber) = newPosition;
		}

		void initialize_neighbour_list(int nNeighbours)
		{
			this->neighbourList = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(this->nAtoms, nNeighbours, -1);
			std::cout<< this->neighbourList << std::endl;
		}

		double * get_neighbourList_data()
		{
			return this->neighbourList.data();
		}

		void print_neighbourList()
		{
			std::cout << this->neighbourList << std::endl;
		}

		// Print positions to screen
		void print_positions()
		{
			std::cout<< "nAtoms: " << this->nAtoms << std::endl;
			std::cout << this->positions << std::endl << std::endl;
		}

		// Set data for already defined matrix object
		void set_positions(int nAtoms, double * positionsArray)
		{
			this->nAtoms = nAtoms;
			this->positionsPointer = positionsArray;

			// Despite appearances, this does not invoke the memory allocator, 
			// because the syntax specifies the location for storing the result.
			new (&(this->positions)) Eigen::Map< Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > 
														(positionsArray, nAtoms, nDim);
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

void set_Atoms_pointer_positions(void * voidAtomsPointer, double * data_array, int numAtoms)
{
	//Cast the pointer as an atoms pointer
	Atoms *atomsPointer = static_cast<Atoms *>(voidAtomsPointer);

	atomsPointer->set_positions(numAtoms, data_array);
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

	const int nRows = 10;
	const int nCols = 3;
	double * testOut = testFunct();

	for (int i = 0; i < nRows; i++)
	{
		for	(int j = 0; j < nCols; j++)
		{
			std::cout << std::setw(6) << testOut[i * nCols + j] << "	";
		}
		std::cout << std::endl;
	}

	std::cout << testOut[0] << std::endl;
	std::cout << Eigen::Map< Eigen::Matrix<double, nRows, nCols, Eigen::RowMajor> > (testOut) << std::endl;


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

	initialize_Atoms_with_positions(&testVoidAtomsPointer, data_array, numAtoms);
	print_Atoms_pointer_positions(testVoidAtomsPointer);
	modify_Atoms_pointer_positions(testVoidAtomsPointer, 3, 2, 100.7);
	print_Atoms_pointer_positions(testVoidAtomsPointer);

	static_cast<Atoms *>(testVoidAtomsPointer)->initialize_neighbour_list(10);
	double * testOut2 = static_cast<Atoms *>(testVoidAtomsPointer)->get_neighbourList_data();


	for (int i = 0; i < numAtoms; i++)
	{
		for	(int j = 0; j < 10; j++)
		{
			std::cout << std::setw(6) << testOut2[i * nCols + j] << "	";
		}
		std::cout << std::endl;
	}

	testOut2[0] = 10;

	static_cast<Atoms *>(testVoidAtomsPointer)->print_neighbourList();
	// destroy_Atoms_void_pointer(testVoidAtomsPointer);

}


//End of extern C
}