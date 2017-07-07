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
// modifyMappedMatrix function
void JointObjectPointer_modifyMappedMatrix(void * voidJointObjectPointer,
                                           int indexRow,
                                           int indexColumn,
                                           double newValue)
{
    //Cast the pointer as an atoms pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    // Modify the value
    joPointer->modifyMappedMatrix(indexRow, indexColumn, newValue);
}


// Given a void pointer to a jointObject instance, call a 
// print Native Matrix function
void JointObjectPointer_printNativeMatrix(void * voidJointObjectPointer)
{
    //Cast the pointer as an atoms pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    joPointer->printNativeMatrix();
}

// Given a void pointer to a jointObject instance, call a 
// print Mapped Matrix function
void JointObjectPointer_printMappedMatrix(void * voidJointObjectPointer)
{
    //Cast the pointer as an atoms pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    joPointer->printMappedMatrix();
}

//Destroy an jointObject pointer masked to by the vPointer
void JointObjectPointer_deleteJointPointer(void * voidJointObjectPointer)
{
    //Cast the pointer as an atoms pointer
    JointObject *joPointer = static_cast<JointObject *>(voidJointObjectPointer);

    delete joPointer;
}

}