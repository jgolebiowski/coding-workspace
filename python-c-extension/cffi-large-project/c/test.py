import unittest

import tst.test_arraymath


def main():
    # initialize
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    # Load tests from modules
    suite.addTest(loader.loadTestsFromModule(tst.test_arraymath))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)


if (__name__ == "__main__"):
    main()
