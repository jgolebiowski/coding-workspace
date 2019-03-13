//
// Created by Jacek Golebiowski on 2019-02-11.
//
#include "arraymath.h"
#include "eigen3/Eigen/dense"


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
        double *dataRES, int matRESrows, int matREScols) {

    EigenMap matA(dataA, matArows, matAcols);
    EigenMap matB(dataB, matBrows, matBcols);
    EigenMap matRES(dataRES, matRESrows, matREScols);
    matRES = matA * matB;
}
