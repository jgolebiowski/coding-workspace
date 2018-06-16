#include <iostream>
#include <Utilities.h>
#include <VectorOperations.h>

int main()
{
    hello_world();
    int size = 10;
    int toAppend = 2;
    std::vector<double> vec = getVector(size);
    printVector(vec);
    appendToVector(vec, toAppend);
    printVector(vec);

    int innerSize = 3;
    int outerSize = 4;
    auto vecOfVecs = getVectorOfVectors(innerSize, outerSize);
    printVectorOfVectors(vecOfVecs);
    appendToEachVector(vecOfVecs, toAppend);
    printVectorOfVectors(vecOfVecs);
}