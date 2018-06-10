import numpy as np
import numba
from timit import timeit

@timeit
def dot_python(a, b):
    n, m = a.shape
    m2, p = b.shape
    if m != m2:
        raise ValueError("arrays must be nxm mxp")

    c = np.empty((n, p))
    for i in range(n):
        for j in range(p):
            c[i, j] = 0
            for k in range(m):
                c[i, j] += a[i, k] * b[k, j]

    return c

@timeit
@numba.jit(nopython=True)
def dot_jit(a, b):
    n, m = a.shape
    m2, p = b.shape
    if m != m2:
        raise ValueError("arrays must be nxm mxp")

    c = np.empty((n, p))
    for i in range(n):
        for j in range(p):
            c[i, j] = 0
            for k in range(m):
                c[i, j] += a[i, k] * b[k, j]

    return c

@timeit
@numba.jit(nopython=True, parallel=True)
def dot_jit_parallel(a, b):
    n, m = a.shape
    m2, p = b.shape
    if m != m2:
        raise ValueError("arrays must be nxm mxp")

    c = np.empty((n, p))
    for i in numba.prange(n):
        for j in numba.prange(p):
            c[i, j] = 0
            for k in range(m):
                c[i, j] += a[i, k] * b[k, j]

    return c


@timeit
def dot_numpy(a, b):
    return np.dot(a, b)


def main():
    n = 3000
    m = 100
    p = 100

    a = np.random.uniform(size=(n, n))
    b = np.random.uniform(size=(n, n))
    c = np.random.uniform(size=(2, 2))
    print("Compiling")
    dot_jit(c, c)
    dot_jit_parallel(c, c)

    print("Testing")
    # c_python = dot_python(a, b)
    c_np = dot_numpy(a, b)
    # c_jit = dot_jit(a, b)
    c_jit_parallel = dot_jit_parallel(a, b)

    # print(np.allclose(c_np, c_python))
    # print(np.allclose(c_np, c_jit))
    print(np.allclose(c_np, c_jit_parallel))



if (__name__ == "__main__"):
    main()
