"""Main file for the problem"""
from numpy_eigen.lib import numpy_eigen
import numpy as np


def main():
    numpy_eigen.hello_world()
    print("------ Matrix from CPP")
    mat = numpy_eigen.getMatrix(4)
    print(mat)
    numpy_eigen.setRandom(mat)
    print(mat)
    mat[0, 2] = 10
    numpy_eigen.printMatrix(mat)

    print("------ Matrix from Python")
    mat = np.random.uniform(0, 1, (3, 4))
    print(mat)
    numpy_eigen.setRandom(mat)
    print(mat)
    mat[2, 1] = 10
    numpy_eigen.printMatrix(mat)

    print("------ Vector of Matrices from CPP")
    vecmat = numpy_eigen.getVectorMatrix(3, 2)
    print(vecmat)
    numpy_eigen.setRandomVectorMatrix(vecmat)
    print(vecmat)
    vecmat[0][2, 1] = 10
    numpy_eigen.printVectorMatrix(vecmat)

    print("------ Vector of Matrices from Python")
    vecmat = [np.zeros((3, 4)) for i in range(2)]
    print(vecmat)
    numpy_eigen.setRandomVectorMatrix(vecmat)
    print(vecmat)
    vecmat[0][2, 1] = 10
    numpy_eigen.printVectorMatrix(vecmat)

    print(numpy_eigen.getVectorMatrix.__doc__)


if (__name__ == "__main__"):
    main()
