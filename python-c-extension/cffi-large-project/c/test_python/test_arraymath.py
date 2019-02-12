import unittest

import numpy as np

from extension.arraymath import matmul


class TestIO(unittest.TestCase):
    def test_matmul(self):
        n, p, m = 200, 400, 500
        A = np.random.uniform(0, 1, size=(n, p))
        B = np.random.uniform(0, 1, size=(p, m))

        C = np.matmul(A, B)
        C2 = matmul(A, B)
        np.testing.assert_allclose(C, C2, atol=1e-5)


if (__name__ == "__main__"):
    unittest.main()