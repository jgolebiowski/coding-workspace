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


class Atoms
{
	Eigen::Map< Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > positions;
	Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> someArray;

	std::vector< std::vector<int> > neighbourList;
	std::vector<int> numNeighbours;

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

			this->neighbourList.resize(nAtoms);
			this->numNeighbours.resize(nAtoms, 0);
		}

		//Empty constructor
		Atoms():
			positions(NULL, 0, 0) 
			{}

		//Simple functions to obtain nAtoms
		inline int get_nAtoms() {return this->nAtoms;}

		//Modify a position
		void modify_position(int atomNumber, int dimNumber, double newPosition)
		{
			this->positions(atomNumber,dimNumber) = newPosition;
		}

		void initialize_someArray(int nColumns)
		{
			this->someArray = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(this->nAtoms, nColumns, -1);
			std::cout<< this->someArray << std::endl;
		}

		double * get_someArray_data()
		{
			return this->someArray.data();
		}

		void print_someArray()
		{
			std::cout << this->someArray << std::endl;
		}

		void initialize_neighbourList()
		{
			int maxNeighs = 2;
			for (unsigned int i = 0; i < this->neighbourList.size(); i++)
			{
				this->neighbourList.at(i).resize(maxNeighs, -1);
				this->numNeighbours.at(i) = maxNeighs;
			}
		}

		void print_neighbourList()
		{
			for (unsigned int i = 0; i < this->neighbourList.size(); i++)
			{
				for	(unsigned int j = 0; j < this->neighbourList.at(i).size(); j++)
				{
					std::cout << std::setw(4) << neighbourList.at(i).at(j) << "	";
				}
				std::cout << std::endl;
			}
		}

		std::vector<int> get_neighbours(int atomNumber)
		{
			return this->neighbourList.at(atomNumber);
		}

		int * get_neighbours_pointer (int atomNumber)
		{
			return this->neighbourList.at(atomNumber).data();
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

	//Test call
	std::cout << std::endl << "Initializing atoms" << std::endl;
	atoms->print_positions();
	// static_cast<Atoms *>(*voidAtomsPointer)->print_positions();

	//Initialize neighbour list with random values
	atoms->initialize_neighbourList();

	// Set the vPointer that the void pointer points to a pointer to Atoms object
	*voidAtomsPointer = static_cast<void *>(atoms);
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

int * get_Atoms_pointer_neighbours_pointer(void * voidAtomsPointer, int atomNumber)
{
	//Cast the pointer as an atoms pointer
	Atoms *atomsPointer = static_cast<Atoms *>(voidAtomsPointer);

	return atomsPointer->get_neighbours_pointer(0);
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

	Atoms *atoms = new Atoms(numAtoms, data_array);
	atoms->initialize_neighbourList();
	atoms->print_neighbourList();

	int * testPoint = atoms->get_neighbours_pointer(0);
	std::cout<< testPoint[0] << std::endl;
	std::cout<< atoms->get_neighbours(0).at(0) << std::endl;
	std::cout<< atoms->get_neighbours(0).data()[0] << std::endl;
}


//End of extern C
}