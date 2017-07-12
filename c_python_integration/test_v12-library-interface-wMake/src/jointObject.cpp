#include <iostream>
#include <Eigen/Dense>
#include <JointObject.h>


extern "C"
{


// Standard constructor prividing a pre-existant array
// Adressing positions in initializaton list is necessary since Map< Matrix<xxx> >
// Does not have an empty constructor, only a (NULL, dim1, dim2) one
JointObject::JointObject(int numRows, int numCols, double * valuesArray):
                mappedMatrix (NULL, 0, 0),
                nRowsMapped (numRows),
                nColsMapped (numCols),
                nRowsNative (numRows),
                nColsNative (numCols)
{
    // Despite appearances, this does not invoke the memory allocator, 
    // because the syntax specifies the location for storing the result.
    new (&(this->mappedMatrix)) Eigen::Map< Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > 
                                                        (valuesArray, numRows, numCols);

    //Initialize the native matrix
    this->nativeMatrix = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(numRows, numCols, 0);
}

// Get the data of a native matrix
double * JointObject::getNativeMatrixData()
{
    return this->nativeMatrix.data();
}

// Set data for already defined matrix object
void JointObject::setMappedMatrixData(int numRows, int numCols, double * valuesArray)
{
    this->nRowsMapped = numRows;
    this->nColsMapped = numCols;
    // Despite appearances, this does not invoke the memory allocator, 
    // because the syntax specifies the location for storing the result.
    new (&(this->mappedMatrix)) Eigen::Map< Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > 
                                                        (valuesArray, numRows, numCols);

}

//modify one of the values of the mapped Matrix
void JointObject::modifyMappedMatrix(int indexRow, int indexColumn, double newValue)
{
    this->mappedMatrix(indexRow, indexColumn) = newValue;
}

//modify one of the values of the native Matrix
void JointObject::modifyNativeMatrix(int indexRow, int indexColumn, double newValue)
{
    this->nativeMatrix(indexRow, indexColumn) = newValue;
}

//print Mapped Matrix
void JointObject::printMappedMatrix()
{
    std::cout << "mappedMatrix w nRowsMapped: "
              << this->nRowsMapped
              << " and nColsMapped: "
              << this->nColsMapped
              << std::endl;
    std::cout << this->mappedMatrix << std::endl << std::endl;
}

//print native Matrix
void JointObject::printNativeMatrix()
{
    std::cout << "nativeMatrix w nRows: "
              << this->nRowsNative
              << " and nCols: "
              << this->nColsNative
              << std::endl;
    std::cout << this->nativeMatrix << std::endl << std::endl;
}

} // End of extern C