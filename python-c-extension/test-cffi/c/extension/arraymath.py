import unittest

import numpy as np
from cffi import FFI

ffi = FFI()

import _project_extension.lib as libextra


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

