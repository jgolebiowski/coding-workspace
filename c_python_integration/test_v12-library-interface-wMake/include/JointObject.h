#pragma once
#include <iostream>
#include <Eigen/Dense>


extern "C"
{

class JointObject
{
    //Matrix that can be initialized from an external pointer
    Eigen::Map< Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> >
            mappedMatrix;
    //Native matrix initialized fro within Cpp
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>
            nativeMatrix;

public:
    //Extra parameters
    int nRowsMapped;
    int nColsMapped;
    int nRowsNative;
    int nColsNative;

    // Standard constructor prividing a pre-existant array
    // Adressing positions in initializaton list is necessary since Map< Matrix<xxx> >
    // Does not have an empty constructor, only a (NULL, dim1, dim2) one
    JointObject(int numRows, int numCols, double * valuesArray);

    //Empty constructor
    JointObject():
        mappedMatrix(NULL, 0, 0)
        {}

    // Get the data of a native matrix
    double * getNativeMatrixData();

    // Set data for already defined matrix object
    void setMappedMatrixData(int numRows, int numCols, double * valuesArray);

    //modify one of the values of the mapped Matrix
    void modifyMappedMatrix(int indexRow, int indexColumn, double newValue);

    //modify one of the values of the native Matrix
    void modifyNativeMatrix(int indexRow, int indexColumn, double newValue);

    //print Mapped Matrix
    void printMappedMatrix();

    //print native Matrix
    void printNativeMatrix();
};

} // End of extern C