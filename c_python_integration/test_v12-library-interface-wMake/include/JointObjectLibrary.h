#pragma once
#include <iostream>
#include <UtilityFunctions.h>
#include <JointObject.h>

extern "C"
{

//Initialize an jointObject instance and assign it to a given pointer
void JointObjectPointer_initializeWithArray(void ** voidjoPointer,
                                            int numRows,
                                            int numCols,
                                            double * valuesArray);

// Given a void pointer to a jointObject instance, call a 
// modifyMappedMatrix function
void JointObjectPointer_modifyMappedMatrix(void * voidJointObjectPointer,
                                           int indexRow,
                                           int indexColumn,
                                           double newValue);


//TODO: Add functions to:
// provide a new (replace) data array(pointer) to the mapped array
// extract the data pointer from the native array


// Given a void pointer to a jointObject instance, call a 
// print Native Matrix function
void JointObjectPointer_printNativeMatrix(void * voidJointObjectPointer);

// Given a void pointer to a jointObject instance, call a 
// print Mapped Matrix function
void JointObjectPointer_printMappedMatrix(void * voidJointObjectPointer);

//Destroy an jointObject pointer masked to by the vPointer
void JointObjectPointer_deleteJointPointer(void * voidJointObjectPointer);

}