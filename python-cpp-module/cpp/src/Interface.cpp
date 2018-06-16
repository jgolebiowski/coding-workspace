#include <iostream>
#include <Eigen/Dense>
#include <Interface.h>

/* Initialize a vctor and return the tuple representation */
myarray myarray_construct(int nRows, int nCols)
{
    auto testMat = new Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
    testMat->setRandom(nRows, nCols);
    std::cout << *testMat <<std::endl;

    myarray out;
    out.n_rows = testMat->rows();
    out.n_cols = testMat->cols();
    out.data = testMat->data();

    return out;
}
