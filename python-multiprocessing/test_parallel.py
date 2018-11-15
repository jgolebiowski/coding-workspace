import unittest
import numpy as np
from parallel import parallel_control, basic_parallel_control


def power(x, power):
    return x ** power


def power2(x, dummy, power):
    return x ** power


def cube(x):
    return x ** 3


class TestParallel(unittest.TestCase):

    def test_simple(self):
        list2process = [(idx,) for idx in range(10)]
        results = parallel_control(cube, list2process, verbose=False)
        for res in results:
            self.assertAlmostEqual(res[1] ** 3, res[0])

    def test_noargs(self):
        num = 3
        list2process = [() for idx in range(10)]
        results = parallel_control(cube, list2process, fixed_args=(num,), verbose=False)
        for res in results:
            self.assertAlmostEqual(num ** 3, res[0])

    def test_fixed_args(self):
        list2process = [(idx,) for idx in range(5)]
        results = parallel_control(power, list2process, fixed_args=(3,), verbose=False)
        for res in results:
            self.assertAlmostEqual(res[1] ** 3, res[0])

    def test_multiple_args(self):
        list2process = [(idx, idx * 2) for idx in range(10)]
        results = parallel_control(power2, list2process, fixed_args=(3,), verbose=False)
        for res in results:
            self.assertAlmostEqual(res[1] ** 3, res[0])

    def test_fork(self):
        list2process = [(idx,) for idx in range(4)]
        results = parallel_control(power, list2process, fixed_args=(3,), start_method="fork", verbose=False)
        for res in results:
            self.assertAlmostEqual(res[1] ** 3, res[0])

    def test_spawn(self):
        list2process = [(idx,) for idx in range(4)]
        results = parallel_control(power, list2process, fixed_args=(3,), start_method="spawn", verbose=False)
        for res in results:
            self.assertAlmostEqual(res[1] ** 3, res[0])

    def test_short(self):
        list2process = [(idx,) for idx in range(1)]
        results = parallel_control(power, list2process, fixed_args=(3,), start_method="spawn", verbose=False)
        for res in results:
            self.assertAlmostEqual(res[1] ** 3, res[0])

    def test_numpy(self):
        list2process = [(np.ones((2, 2)) * idx,) for idx in range(5)]
        results = parallel_control(power, list2process, fixed_args=(3,), start_method="spawn", verbose=False)
        for res in results:
            self.assertTrue(np.allclose(res[1] ** 3, res[0]))


class TestBasicParallel(unittest.TestCase):
    def test_basic_simple(self):
        list2process = [(idx,) for idx in range(10)]
        results = basic_parallel_control(cube, list2process, verbose=False)
        for idx in range(len(list2process)):
            self.assertAlmostEqual(list2process[idx][0] ** 3, results[idx])

    def test_basic_noargs(self):
        num = 3
        list2process = [() for idx in range(10)]
        results = basic_parallel_control(cube, list2process, fixed_args=(num,), verbose=False)
        for idx in range(len(list2process)):
            self.assertAlmostEqual(num ** 3, results[idx])

    def test_basic_fixed_args(self):
        list2process = [(idx,) for idx in range(5)]
        results = basic_parallel_control(power, list2process, fixed_args=(3,), verbose=False)
        for idx in range(len(list2process)):
            self.assertAlmostEqual(list2process[idx][0] ** 3, results[idx])

    def test_basic_multiple_args(self):
        list2process = [(idx, idx * 2) for idx in range(10)]
        results = basic_parallel_control(power2, list2process, fixed_args=(3,), verbose=False)
        for idx in range(len(list2process)):
            self.assertAlmostEqual(list2process[idx][0] ** 3, results[idx])

    def test_basic_fork(self):
        list2process = [(idx,) for idx in range(4)]
        results = basic_parallel_control(power, list2process, fixed_args=(3,), start_method="fork", verbose=False)
        for idx in range(len(list2process)):
            self.assertAlmostEqual(list2process[idx][0] ** 3, results[idx])

    def test_basic_spawn(self):
        list2process = [(idx,) for idx in range(4)]
        results = basic_parallel_control(power, list2process, fixed_args=(3,), start_method="spawn", verbose=False)
        for idx in range(len(list2process)):
            self.assertAlmostEqual(list2process[idx][0] ** 3, results[idx])

    def test_basic_short(self):
        list2process = [(idx,) for idx in range(1)]
        results = basic_parallel_control(power, list2process, fixed_args=(3,), start_method="spawn", verbose=False)
        for idx in range(len(list2process)):
            self.assertAlmostEqual(list2process[idx][0] ** 3, results[idx])

    def test_basic_numpy(self):
        list2process = [(np.ones((2, 2)) * idx,) for idx in range(5)]
        results = basic_parallel_control(power, list2process, fixed_args=(3,), start_method="spawn", verbose=False)
        for idx in range(len(list2process)):
            self.assertTrue(np.allclose(list2process[idx][0] ** 3, results[idx]))


if (__name__ == "__main__"):
    unittest.main()
