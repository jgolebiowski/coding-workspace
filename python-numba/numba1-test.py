import numpy as np
import numba
from timit import timeit


def sum2d(array):
    m, n = array.shape
    result = 0.0
    for i in range(m):
        for j in range(n):
            result += array[i, j]

    return result


@timeit
@numba.jit(nopython=True)
def sum2d_jit(array):
    m, n = array.shape
    result = 0.0
    for i in range(m):
        for j in range(n):
            result += array[i, j]

    return result


@timeit
@numba.jit(nopython=True, parallel=True)
def sum2d_jit_parallel(array):
    m, n = array.shape
    result = 0.0
    for i in numba.prange(m):
        for j in numba.prange(n):
            result += array[i, j]

    return result


@timeit
def test_numpy(arr):
    np.sum(arr)


def main():
    N = 3000
    arr = np.random.uniform(size=(N, N))
    print("Compiling")
    sum2d_jit(arr)
    sum2d_jit_parallel(arr)

    print("Testing")
    test_numpy(arr)
    sum2d_jit(arr)
    sum2d_jit_parallel(arr)


if (__name__ == "__main__"):
    main()
