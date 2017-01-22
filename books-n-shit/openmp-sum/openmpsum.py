import numpy as np
from scipy import weave

def openmpSum(in_array):
    """
    Performs fast sum of an array using openmm
    """
    a = np.asarray(in_array)
    b = np.array([1.])
    N = int(np.prod(a.shape))
    code = r"""
    int i=0;
    double sum = 0;
    omp_set_num_threads(12);
    #pragma omp parallel for default(shared) private(i) reduction(+:sum)
        for (i=0; i<N; i++)
              sum += a[i];
    b[0] = sum;
    """
    weave.inline(code, ['a','N','b'],
                     extra_compile_args=['-march=native  -O3  -fopenmp ' ],
                     support_code = r"""
    #include <stdio.h>
    #include <omp.h>
    #include <math.h>""",
     libraries=['gomp'])
    return b[0]


def sum1(arr_in):
    """
    Performs fast sum of an array using openmm
    """
    assert arr_in.ndim == 2
    assert arr_in.dtype == 'float32'
    n_rows, n_cols = map(int, arr_in.shape)
    arr_in = np.asarray(arr_in)
    arr_out = np.empty(n_rows, dtype=arr_in.dtype)
    code = r"""
    int i, j;
    float sum;
    omp_set_num_threads(8);
    #pragma omp parallel for default(shared) private(j)
    for(j=0; j<n_rows; ++j) {
        sum = 0;
        //#pragma omp parallel for default(shared) private(i) reduction(+:sum)
        for(i=0; i<n_cols; ++i)
            sum += arr_in[j*n_cols + i];
        arr_out[j] = sum;
    }
    """
    weave.inline(
        code,
        ['arr_in','arr_out','n_rows', 'n_cols'],
        extra_compile_args=[
            "-fopenmp",
            "-pthread",
            "-O6",
            "-march=native",
            "-mtune=native",
            "-funroll-all-loops",
            "-fomit-frame-pointer",
            "-march=native",
            "-mtune=native",
            "-msse4",
            "-ftree-vectorize",
            "-ftree-vectorizer-verbose=5",
            "-ffast-math",
            "-ftree-loop-distribution",
            "-funroll-loops",
            "-ftracer",

        ],
        verbose=2,
        support_code = \
        r"""
        #include <stdio.h>
        #include <omp.h>
        #include <math.h>
        """,
     libraries=['gomp'])
    return arr_out

a = np.random.randn(1e6, 12).astype('f')

import time
N_ITERATIONS = 100

gv = sum1(a)
start = time.time()
for i in xrange(N_ITERATIONS):
    gv = sum1(a)
end = time.time()
print end - start

start = time.time()
for i in xrange(N_ITERATIONS):
    gt = a.sum(1)
end = time.time()
print end - start

assert np.linalg.norm(gv - gt) < 1e-3
