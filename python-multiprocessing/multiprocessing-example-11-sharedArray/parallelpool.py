import multiprocessing
import multiprocessing.sharedctypes
import numpy as np
from typing import List


class SharedArray(object):
    def __init__(self, shape: List[int]=None, dtype: str="float32", fromnumpy: np.array=None):
        if fromnumpy is not None:
            result = np.ctypeslib.as_ctypes(fromnumpy)
            self.array = multiprocessing.sharedctypes.Array(result._type_, result, lock=False)
            self.shape = fromnumpy.shape
            self.dtype = fromnumpy.dtype
        else:
            if dtype == "float32":
                self.array = multiprocessing.Array("f", int(np.prod(shape)), lock=False)
            elif dtype == "double":
                self.array = multiprocessing.Array("d", int(np.prod(shape)), lock=False)
            elif dtype == "int":
                self.array = multiprocessing.Array("i", int(np.prod(shape)), lock=False)
            else:
                raise ValueError("Only supports float32, double and int")
            self.dtype=dtype
            self.shape=shape

    def tonumpy(self):
        return np.ctypeslib.as_array(self.array, shape=self.shape).reshape(self.shape)

    @staticmethod
    def fromnumpy(array):
        result = np.ctypeslib.as_ctypes(array)
        array = multiprocessing.Array(result._type_, result, lock=False)


def operate(rank: int):
    x = shared_array.tonumpy()
    print(x.shape)
    x[0, :, rank] = rank

def main():
    list2process = [(idx,) for idx in range(10)]
    number_of_workers = 2
    x = np.random.uniform(0, 1, (1, 2, 10))
    array = SharedArray(fromnumpy=x)

    def helper_init(process_array):
        global shared_array
        shared_array = process_array

    pool = multiprocessing.Pool(processes=number_of_workers,
                initializer=helper_init,
                initargs=(array, ))
    pool.map_async(operate, list2process)
    pool.close()
    pool.join()
    print(array.tonumpy())


if (__name__ == "__main__"):
    main()
