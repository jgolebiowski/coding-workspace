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


def modify_element(lister, idx):
    lister[idx] = "yo"

@numba.jit(nopython=True, parallel=True)
def modify_list(lister, length):

    for idx in numba.prange(length):
        modify_element(lister, idx)



def main():
    a = np.arange(10)

    print("A0:", a)
    b = test_parallel(a)
    print("A1:", a)
    print("B1:", b)

    lister = np.array(["abc" for idx in range(int(10 ** 8))])
    modify_list(lister, len(lister))
    print(lister[0: 10], len(lister))


if (__name__ == "__main__"):
    main()
