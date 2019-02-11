#include <gsl/gsl_matrix.h>
#include <gsl/gsl_blas.h>
#include "stdio.h"



void arraymath_matmul(
        double *matA, int matAcols, int matArows,
        double *matB, int matBcols, int matBrows,
        double *matRES, int matREScols, int matRESrows) 
{

    gsl_matrix_view A = gsl_matrix_view_array(matA, matAcols, matArows);
    gsl_matrix_view B = gsl_matrix_view_array(matB, matBcols, matBrows);
    gsl_matrix_view RES = gsl_matrix_view_array(matRES, matREScols, matRESrows);

    double alpha = 1.0;
    double beta = 0.0;

    gsl_blas_dgemm(CblasNoTrans, CblasNoTrans,
                   alpha, &A.matrix, &B.matrix,
                   beta, &RES.matrix);
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


    gsl_matrix_view RES = gsl_matrix_view_array(c, 2, 2);
    gsl_matrix_fprintf(stdout, &RES.matrix, "%f");
}
