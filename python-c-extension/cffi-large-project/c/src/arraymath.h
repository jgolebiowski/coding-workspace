//
// Created by Jacek Golebiowski on 2019-02-11.
//

#ifndef PROJECT_EXTENSION_ARRAYMATH_H
#define PROJECT_EXTENSION_ARRAYMATH_H

/**
 * This function assigns matRES = matA @ matB
 * @param matA Data for the input matrix
 * @param matAcols Dimensions for the input matrix
 * @param matArows Dimensions for the input matrix
 * @param matB Data for the input matrix
 * @param matBcols Dimensions for the input matrix
 * @param matBrows Dimensions for the input matrix
 * @param matRES Data for the output matrix
 * @param matREScols Dimensions for the output matrix
 * @param matRESrows Dimensions for the output matrix
 */
void arraymath_matmul(
        double *matA, int matAcols, int matArows,
        double *matB, int matBcols, int matBrows,
        double *matRES, int matREScols, int matRESrows);

#endif //PROJECT_EXTENSION_ARRAYMATH_H
