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
//    EigenDynamicRowMajor &getMatrix(int size);
    m.def("getMatrix",
          &getMatrix,
          " * @brief Generate a new Matrix of zeros\n"
          " * @param size size of the matrix\n"
          " * @return the created vector",
          py::arg("size"),
          py::return_value_policy::reference_internal);

/**
 * @brief Set matrix elements to random values
 * @param mat the matrix in question
 */
//    void setRandom(EigenRefDynamicRowMajor &mat);
    m.def("setRandom",
          &setRandom,
          " * @brief Set matrix elements to random values\n"
          " * @param mat the matrix in question",
          py::arg("mat").noconvert());

/**
 * @brief Print a given matrix
 * @param mat Matrix in question
 */
//    void printMatrix(EigenRefDynamicRowMajor &mat);
    m.def("printMatrix",
          &printMatrix,
          " * @brief Print a given matrix\n"
          " * @param mat Matrix in question",
          py::arg("mat").noconvert());

/**
 * @brief Get a vector of matrixes of given size
 * @param size Matrix size
 * @param length Vector length
 * @return Created vector
 */
//    std::vector<EigenDynamicRowMajor> &getVectorMatrix(
//            int size, int length);
    m.def("getVectorMatrix",
          &getVectorMatrix,
          " * @brief Get a vector of matrixes of given size\n"
          " * @param size Matrix size\n"
          " * @param length Vector length\n"
          " * @return Created vector",
          py::arg("size"),
          py::arg("length"),
          py::return_value_policy::reference_internal);

/**
 * @brief For every matrix in a vector, matrix elements to random values
 * @param vectorMatrix the vector of matrices in question
 */
//    void setRandomVectorMatrix(
//            std::vector<EigenRefDynamicRowMajor> &vectorMatrix);
    m.def("setRandomVectorMatrix",
          &setRandomVectorMatrix,
          " * @brief For every matrix in a vector, matrix elements to random values\n"
          " * @param vectorMatrix the vector of matrices in question",
          py::arg("vectorMatrix").noconvert());

/**
 * @brief Print the vector of matrices
 * @param vectorMatrix the vector of matrices in question
 */
//    void printVectorMatrix(
//            std::vector<EigenRefDynamicRowMajor> &vectorMatrix);
    m.def("printVectorMatrix",
          &printVectorMatrix,
          " * @brief Print the vector of matrices\n"
          " * @param vectorMatrix the vector of matrices in question",
          py::arg("vectorMatrix").noconvert());
}

