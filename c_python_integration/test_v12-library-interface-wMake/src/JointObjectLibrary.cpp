#include <iostream>
#include <UtilityFunctions.h>
#include <JointObject.h>

extern "C"
{

//Initialize an jointObject instance and assign it to a given pointer
void JointObjectPointer_initializeWithArray(void ** voidjoPointer,
                                            int numRows,
                                            int numCols,
                                            double * valuesArray)
{
    
    JointObject *myJointObject = new JointObject(numRows, numCols, valuesArray);

    // Set the vPointer that the void pointer points to a pointer to JointObject object
    *voidjoPointer = static_cast<void *>(myJointObject);
}

// Given a void pointer to a jointObject instance, call a
// setMappedMatrixData function that:
// Sets data for already defined matrix object
void JointObjectPointer_setMappedMatrixData(void * voidJointObjectPointer,
                                            int numRows,
                                            int numCols,
                                            double * valuesArray)
{
    //Cast the void pointer as a JointObject pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    // Modify the values
    joPointer->setMappedMatrixData(numRows, numCols, valuesArray);
}

// Given a void pointer to a jointObject instance,
// Obtain the dimensions of the Native array
void JointObjectPointer_getNativeDimensions(void * voidJointObjectPointer,
                                            int * numRows,
                                            int * numCols)
{
    //Cast the void pointer as a JointObject pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    // Get the values
    (*numRows) = joPointer->nRowsNative;
    (*numCols) = joPointer->nColsNative;
}

// Given a void pointer to a jointObject instance,
// Obtain the data of the Native array
double * JointObjectPointer_getNativeMatrixData(void * voidJointObjectPointer)
{
    //Cast the void pointer as a JointObject pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    // Get the values
    return joPointer->getNativeMatrixData();
}

// Given a void pointer to a jointObject instance, call a 
// modifyMappedMatrix function
void JointObjectPointer_modifyMappedMatrix(void * voidJointObjectPointer,
                                           int indexRow,
                                           int indexColumn,
                                           double newValue)
{
    //Cast the void pointer as a JointObject pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    // Modify the value
    joPointer->modifyMappedMatrix(indexRow, indexColumn, newValue);
}

// Given a void pointer to a jointObject instance, call a 
// modifyNativeMatrix function
void JointObjectPointer_modifyNativeMatrix(void * voidJointObjectPointer,
                                           int indexRow,
                                           int indexColumn,
                                           double newValue)
{
    //Cast the void pointer as a JointObject pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    // Modify the value
    joPointer->modifyNativeMatrix(indexRow, indexColumn, newValue);
}


// Given a void pointer to a jointObject instance, call a 
// print Native Matrix function
void JointObjectPointer_printNativeMatrix(void * voidJointObjectPointer)
{
    //Cast the void pointer as a JointObject pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    joPointer->printNativeMatrix();
}

// Given a void pointer to a jointObject instance, call a 
// print Mapped Matrix function
void JointObjectPointer_printMappedMatrix(void * voidJointObjectPointer)
{
    //Cast the void pointer as a JointObject pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    joPointer->printMappedMatrix();
}

//Destroy an jointObject pointer masked to by the vPointer
void JointObjectPointer_deleteJointPointer(void * voidJointObjectPointer)
{
    //Cast the void pointer as a JointObject pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    delete joPointer;
}

}