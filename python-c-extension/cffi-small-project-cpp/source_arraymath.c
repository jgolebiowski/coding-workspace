#include "eigen3/Eigen/dense"
#include <iostream>

typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> EigenMatrixXdRowMajor;
typedef Eigen::Map<EigenMatrixXdRowMajor> EigenMap;

/**
 * This function assigns matRES = matA @ matB
 * @param dataA Data for the input matrix
 * @param matArows Dimensions for the input matrix
 * @param matAcols Dimensions for the input matrix
 * @param dataB Data for the input matrix
 * @param matBrows Dimensions for the input matrix
 * @param matBcols Dimensions for the input matrix
 * @param dataRES Data for the output matrix
 * @param matRESrows Dimensions for the output matrix
 * @param matREScols Dimensions for the output matrix
 */
extern "C"
void arraymath_matmul(
        double *dataA, int matArows, int matAcols,
        double *dataB, int matBrows, int matBcols,
        double *dataRES, int matRESrows, int matREScols)
{

    EigenMap matA(dataA, matArows, matAcols);
    EigenMap matB(dataB, matBrows, matBcols);
    EigenMap matRES(dataRES, matRESrows, matREScols);
    matRES = matA * matB;
}

int main() {
    double a[] = {0.11, 0.12, 0.13,
                  0.21, 0.22, 0.23};

    double b[] = {1011, 1012,
                  1021, 1022,
                  1031, 1032};

    double c[] = {0.00, 0.00,
                  0.00, 0.00};
    arraymath_matmul(a, 2, 3,
                     b, 3, 2,
                     c, 2, 2);
    EigenMap matC(c, 2, 2);
    std::cout << matC << std::endl;
}
