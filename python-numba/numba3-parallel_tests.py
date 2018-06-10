import numpy as np
import numba
from timit import timeit


@numba.jit(nopython=True, parallel=True)
def test_parallel(a):
    test = 0
    n_iter = a.size
    test = 0
    test_arr = np.empty(a.size)

    for idx in numba.prange(n_iter):
        # print("Modifying the list", idx, "out of", n_iter)
        test = idx ** 2 + 1
        test_arr[idx] = test

    print(test)
    return test_arr


@numba.jit(nopython=False, parallel=True)
def modify_list(lister, length):

    for idx in numba.prange(length):
        lister[idx] = "yo"



def main():
    a = np.arange(10)

    print("A0:", a)
    b = test_parallel(a)
    print("A1:", a)
    print("B1:", b)

    lister = np.array("This eBook is for the use of anyone anywhere at no cost and withk".split())
    modify_list(lister, len(lister))
    print(lister)


if (__name__ == "__main__"):
    main()
