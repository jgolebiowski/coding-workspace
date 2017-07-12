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
// setMappedMatrixData function that:
// Sets data for already defined matrix object
void JointObjectPointer_setMappedMatrixData(void * voidJointObjectPointer,
                                            int numRows,
                                            int numCols,
                                            double * valuesArray);

// Given a void pointer to a jointObject instance,
// Obtain the dimensions of the Native array
void JointObjectPointer_getNativeDimensions(void * voidJointObjectPointer,
                                            int * numRows,
                                            int * numCols);

// Given a void pointer to a jointObject instance,
// Obtain the data of the Native array
double * JointObjectPointer_getNativeMatrixData(void * voidJointObjectPointer);

// Given a void pointer to a jointObject instance, call a 
// modifyMappedMatrix function
void JointObjectPointer_modifyMappedMatrix(void * voidJointObjectPointer,
                                           int indexRow,
                                           int indexColumn,
                                           double newValue);

// Given a void pointer to a jointObject instance, call a 
// modifyNativeMatrix function
void JointObjectPointer_modifyNativeMatrix(void * voidJointObjectPointer,
                                           int indexRow,
                                           int indexColumn,
                                           double newValue);

// Given a void pointer to a jointObject instance, call a 
// print Native Matrix function
void JointObjectPointer_printNativeMatrix(void * voidJointObjectPointer);

// Given a void pointer to a jointObject instance, call a 
// print Mapped Matrix function
void JointObjectPointer_printMappedMatrix(void * voidJointObjectPointer);

//Destroy an jointObject pointer masked to by the vPointer
void JointObjectPointer_deleteJointPointer(void * voidJointObjectPointer);

}