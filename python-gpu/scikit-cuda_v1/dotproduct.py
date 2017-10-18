import pycuda.autoinit
import pycuda.gpuarray as gpuarray
import numpy as np
import skcuda.linalg
skcuda.linalg.init()

N = int(100)
a = np.asarray(np.random.rand(N, N), dtype=np.float32, order="F")
b = np.asarray(np.random.rand(N, N), dtype=np.float32)
c = np.asarray(np.random.rand(N, N))
d = np.asarray(np.random.rand(N, N))

a = a.astype(np.float32, order="C")
b = b.astype(np.float32, order="C")
a_gpu = gpuarray.to_gpu(a)
b_gpu = gpuarray.to_gpu(b)

def matmul(a, b):
    a = a.astype(np.float32, order="C")
    b = b.astype(np.float32, order="C")
    a_gpu = gpuarray.to_gpu(a)
    b_gpu = gpuarray.to_gpu(b)

    c_gpu = skcuda.linalg.dot(a_gpu, b_gpu)
    return c_gpu.get()
