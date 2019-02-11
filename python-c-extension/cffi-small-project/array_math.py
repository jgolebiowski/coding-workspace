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



if __name__ == '__main__':
    C_HEADER = """
    void arraymath_matmul(
        double *matA, int matAcols, int matArows,
        double *matB, int matBcols, int matBrows,
        double *matRES, int matREScols, int matRESrows);
    """
    SOURCES = ["source_arraymath.c"]

    compile_cffi("_array_math", C_HEADER, C_HEADER, SOURCES)
    unittest.main()
