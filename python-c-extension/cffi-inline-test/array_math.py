import unittest

import numpy as np
from cffi import FFI

ffi = FFI()

from compile import compile_cffi
import _array_math.lib as libextra


def matmul(A, B):
    """
    Run matrix multiply, A @ B
    :param A: Input Array
    :param B: Input array
    :return: result
    """
    n, p1 = A.shape
    p2, m = B.shape

    C = np.empty((n, m))
    libextra.arraymath_matmul(
        ffi.cast("double *", ffi.from_buffer(A)), n, p1,
        ffi.cast("double *", ffi.from_buffer(B)), p2, m,
        ffi.cast("double *", ffi.from_buffer(C)), n, m
    )
    return C


class TestIO(unittest.TestCase):
    def test_matmul(self):
        n, p, m = 200, 400, 500
        A = np.random.uniform(0, 1, size=(n, p))
        B = np.random.uniform(0, 1, size=(p, m))

        C = np.matmul(A, B)
        C2 = matmul(A, B)
        np.testing.assert_allclose(C, C2, atol=1e-5)


CHEADER = """
void arraymath_matmul(
        double *matA, int matAcols, int matArows,
        double *matB, int matBcols, int matBrows,
        double *matRES, int matREScols, int matRESrows);
"""
CCODE = r"""
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_blas.h>

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
"""

if __name__ == '__main__':
    compile_cffi("_array_math", CHEADER, CCODE)
    unittest.main()
