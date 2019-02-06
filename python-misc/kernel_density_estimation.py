import unittest
import numpy as np
from typing import Tuple, Callable


def kde(x: np.ndarray, kernel: Callable, bandwidth: float, npoints: int = 100,
        xlim: Tuple[float, float] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Run kernel density estimation on a given sample, returning the approximate distribution
    :param x: Sample in shape (nexamples, )
    :param kernel: the kernel function, can be found here
    :param bandwidth: kernel bandwith
    :param npoints: number of gridpoints for the approximation
    :param xlim: Limit for the arguments  given as (minium, maximum)
    :return:
        - distribution arguments
        - distribution likelihood
    """
    nexamples = len(x)
    if xlim is None:
        mini = np.min(x) - bandwidth
        maxi = np.max(x) + bandwidth
    else:
        mini, maxi = xlim

    arguments = np.linspace(mini, maxi, num=npoints, endpoint=True)
    kernel_values = kernel(x, arguments, bandwidth) / (nexamples * bandwidth)
    values = np.sum(kernel_values, axis=0)
    return arguments, values


def kernel_triangular(x: np.ndarray, y: np.ndarray, bandwidth: float) -> np.ndarray:
    """
    Simple triangular kernel between two set of points

    :param x: First set of points in shape (nexamples, )
    :param y: Second set of points (npoints)
    :param bandwidth: kernel bandwidth
    :return: Kernel values between all combinations in shape (nexamples, npoints)
    """
    res = np.subtract.outer(x, y) / bandwidth
    res = 1 - np.abs(res)
    return res


def kernel_gaussian(x: np.ndarray, y: np.ndarray, bandwidth: float) -> np.ndarray:
    """
    Simple triangular kernel between two set of points

    :param x: First set of points in shape (nexamples, )
    :param y: Second set of points (npoints)
    :param bandwidth: kernel bandwidth
    :return: Kernel values between all combinations in shape (nexamples, npoints)
    """
    res = np.subtract.outer(x, y) / bandwidth
    res = np.exp(- np.square(res) / 2) / np.sqrt(np.pi * 2)
    return res


class KernelDensityEstimationTest(unittest.TestCase):
    def test_kde(self):
        sample = np.random.normal(0, 1, size=1000)
        args, vals = kde(sample, kernel_gaussian, bandwidth=0.4, npoints=100, xlim=(-5, 5))

        try:
            from sklearn.neighbors import KernelDensity
            kde_sk = KernelDensity(kernel='gaussian', bandwidth=0.4).fit(sample.reshape(-1, 1))
            density = kde_sk.score_samples(args.reshape(-1, 1))
            density = np.exp(density)
            np.testing.assert_allclose(vals, density)
        except ImportError:
            pass

    def test_kernel_triangular(self):
        size = 5
        band = 0.5
        x = np.random.uniform(0, 1, size=size)
        y = np.random.uniform(0, 1, size=size)
        vals = kernel_triangular(x, y, band)
        for i in range(size):
            for j in range(size):
                target = (1 - np.abs(x[i] - y[j]) / band)
                self.assertAlmostEqual(vals[i, j], target, delta=1e-5)

    def test_kernel_gaussian(self):
        size = 5
        band = 0.5
        x = np.random.uniform(0, 1, size=size)
        y = np.random.uniform(0, 1, size=size)
        vals = kernel_gaussian(x, y, band)
        for i in range(size):
            for j in range(size):
                dist = np.abs(x[i] - y[j]) / band
                target = np.exp(- np.square(dist) / 2) / np.sqrt(np.pi * 2)
                self.assertAlmostEqual(vals[i, j], target, delta=1e-5)


if (__name__ == "__main__"):
    unittest.main()
