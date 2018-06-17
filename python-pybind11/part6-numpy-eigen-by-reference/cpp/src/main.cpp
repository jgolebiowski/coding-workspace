#include <iostream>
#include <Utilities.h>
#include <MatrixOperations.h>

int main()
{
    hello_world();
    int size = 3;
    EigenDynamicRowMajor mat = getMatrix(size);
    printMatrix(mat);
    setRandom(mat);
    printMatrix(mat);

    int length = 2;
    auto vecMat = getVectorMatrix(size, length);
    printVectorMatrix(vecMat);
    setRandomVectorMatrix(vecMat);
    printVectorMatrix(vecMat);


}