#include <iostream>
#include <UtilityFunctions.h>
#include <JointObject.h>
#include <JointObjectLibrary.h>


int main()
{
	std::cout << "Welcome to my new program!" << std::endl;
	int rowsN = 4;
	int colsN = 5;
	int elemN = colsN * rowsN;
	double data_array[elemN];

	for (int i = 0; i < rowsN; i++)
	for	(int j = 0; j < colsN; j++)
	{
		data_array[i * colsN + j] = i * colsN + j;
	}
	std::cout << "Created the data array" << std::endl;

    JointObject myTestObject(rowsN, colsN, data_array);
    myTestObject.printMappedMatrix();
    myTestObject.printNativeMatrix();

    for (int i = 0; i < rowsN; i++)
    for (int j = 0; j < colsN; j++)
    {
        myTestObject.modifyNativeMatrix(i, j, i * 10 + j);
    }
    myTestObject.printNativeMatrix();

    double * tempPointer = myTestObject.getNativeMatrixData();
    tempPointer[1] = 100;
    myTestObject.printNativeMatrix();


    // ------ Set the vPointer so that the void pointer 
    // ------ points to a pointer to JointObject object
    std::cout << "Set the vPointer from instance of jo!" << std::endl;
    // Initialize a vPointer
    void *testJOvoidPointer;
    // Initialize a JOpointer
    JointObject * joPointer = &myTestObject;
    // Cast a joPointer to a void pointer
    testJOvoidPointer = static_cast<void *>(joPointer);

    //Run the function
    JointObjectPointer_printNativeMatrix(testJOvoidPointer);
    myTestObject.modifyNativeMatrix(0, 1, 55);
    JointObjectPointer_printNativeMatrix(testJOvoidPointer);
    JointObjectPointer_printMappedMatrix(testJOvoidPointer);

    // ------ Initialize a jointObject pointer
    // ------ and automatically assign it to a vPointer
    std::cout << "Set the vPointer by init function!" << std::endl;
    // create a new voindpointer
    void *secondTestJOvoidPointer;

    // Use the initialization function to generate new object 
    JointObjectPointer_initializeWithArray(&secondTestJOvoidPointer,
                                            rowsN,
                                            colsN,
                                            data_array);
    JointObjectPointer_printNativeMatrix(secondTestJOvoidPointer);
    JointObjectPointer_printMappedMatrix(secondTestJOvoidPointer);

    //Delete a jo instance
    JointObjectPointer_deleteJointPointer(secondTestJOvoidPointer);
	return 0;
}