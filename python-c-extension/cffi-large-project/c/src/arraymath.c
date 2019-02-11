//
// Created by Jacek Golebiowski on 2019-02-11.
//
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_blas.h>

#include "arraymath.h"


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
        double *matRES, int matREScols, int matRESrows) {

    gsl_matrix_view A = gsl_matrix_view_array(matA, matAcols, matArows);
    gsl_matrix_view B = gsl_matrix_view_array(matB, matBcols, matBrows);
    gsl_matrix_view RES = gsl_matrix_view_array(matRES, matREScols, matRESrows);

    double alpha = 1.0;
    double beta = 0.0;

    gsl_blas_dgemm(CblasNoTrans, CblasNoTrans,
                   alpha, &A.matrix, &B.matrix,
                   beta, &RES.matrix);
}
