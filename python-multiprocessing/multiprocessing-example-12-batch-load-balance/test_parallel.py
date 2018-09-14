import unittest
import numpy as np
from parallel import parallel_control


def power(x, power):
    return x ** power


def power2(x, dummy, power):
    return x ** power


def cube(x):
    return x ** 3


class TestParallel(unittest.TestCase):

    def test_simple(self):
        list2process = [(idx,) for idx in range(10)]
        results = parallel_control(cube, list2process)
        for res in results:
            self.assertAlmostEqual(res[0][0] ** 3, res[1])

    def test_fixed_args(self):
        list2process = [(idx,) for idx in range(5)]
        results = parallel_control(power, list2process, fixed_args=(3,))
        for res in results:
            self.assertAlmostEqual(res[0][0] ** 3, res[1])

    def test_multiple_args(self):
        list2process = [(idx, idx * 2) for idx in range(10)]
        results = parallel_control(power2, list2process, fixed_args=(3,))
        for res in results:
            self.assertAlmostEqual(res[0][0] ** 3, res[1])

    def test_fork(self):
        list2process = [(idx,) for idx in range(4)]
        results = parallel_control(power, list2process, fixed_args=(3,), start_method="fork")
        for res in results:
            self.assertAlmostEqual(res[0][0] ** 3, res[1])

    def test_spawn(self):
        list2process = [(idx,) for idx in range(4)]
        results = parallel_control(power, list2process, fixed_args=(3,), start_method="spawn")
        for res in results:
            self.assertAlmostEqual(res[0][0] ** 3, res[1])

    def test_short(self):
        list2process = [(idx,) for idx in range(1)]
        results = parallel_control(power, list2process, fixed_args=(3,), start_method="spawn")
        for res in results:
            self.assertAlmostEqual(res[0][0] ** 3, res[1])

    def test_numpy(self):
        list2process = [(np.ones((2, 2)) * idx,) for idx in range(5)]
        results = parallel_control(power, list2process, fixed_args=(3,), start_method="spawn")
        for res in results:
            self.assertTrue(np.allclose(res[0][0] ** 3, res[1]))

if (__name__ == "__main__"):
    unittest.main()
