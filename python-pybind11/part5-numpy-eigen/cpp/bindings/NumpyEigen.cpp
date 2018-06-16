//
// Created by Golebiowski, Jacek on 6/16/18.
////
#include <Utilities.h>
#include <MatrixOperations.h>

#include <Eigen/Dense>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/eigen.h>


namespace py = pybind11;

// Here, the first argument is the module name which must be the same as cmake project name!!
PYBIND11_MODULE(numpy_eigen, m)
{

//    Provide module documentation
    m.doc() = "numpy_eigen plugin: testing conversions"; // optional module docstring

/**
 * @brief Print Hello world
 */
//    void hello_world();
    m.def("hello_world",
          &hello_world,
          "Print hello world");
/**
 * @brief Generate a new Matrix of zeros
 * @param size size of the matrix
 * @return the created vector
 */
//    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> &getMatrix(int size);
    m.def("getMatrix",
          &getMatrix,
          "Generate a new Matrix of zeros",
          py::arg("size of the matrix"),
          py::return_value_policy::take_ownership);

/**
 * @brief Set matrix elements to random values
 * @param mat the matrix in question
 */
//    void setRandom(Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> &mat);
    m.def("setRandom",
          &setRandom,
          "Set matrix elements to random values",
          py::arg("Matrix in question"));

/**
 * @brief Print a given matrix
 * @param mat Matrix in question
 */
//    void printMatrix(Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> &mat);
    m.def("printMatrix",
          &printMatrix,
          "Print a given matrix",
          py::arg("Matrix in question"));

/**
 * @brief Get a vector of matrixes of given size
 * @param size Matrix size
 * @param length Vector length
 * @return Created vector
 */
//    std::vector<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> &getVectorMatrix(
//            int size, int length);
    m.def("getVectorMatrix",
          &getVectorMatrix,
          "Get a vector of matrixes of given size",
          py::arg("Matrix size"),
          py::arg("Vector length"),
          py::return_value_policy::reference_internal);

/**
 * @brief For every matrix in a vector, matrix elements to random values
 * @param vectorMatrix the vector of matrices in question
 */
//    void setRandomVectorMatrix(
//            std::vector<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> &vectorMatrix);
    m.def("setRandomVectorMatrix",
          &setRandomVectorMatrix,
          "For every matrix in a vector, matrix elements to random values",
          py::arg("the vector of matrices in question"));

/**
 * @brief Print the vector of matrices
 * @param vectorMatrix the vector of matrices in question
 */
//    void printVectorMatrix(
//            std::vector<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> &vectorMatrix);
    m.def("printVectorMatrix",
          &printVectorMatrix,
          "Print the vector of matrices",
          py::arg("the vector of matrices in question"));
}

