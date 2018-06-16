//
// Created by Golebiowski, Jacek on 6/16/18.
////
#include <Utilities.h>
#include <VectorOperations.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>


// Make some datatyped opaque, now they can be passed by reference
PYBIND11_MAKE_OPAQUE(std::vector<double>)
PYBIND11_MAKE_OPAQUE(std::vector<std::vector<double>>)

namespace py = pybind11;

// Here, the first argument is the module name which must be the same as cmake project name!!
PYBIND11_MODULE(stl_containers, m)
{
//    Specify the bindings for opaque datatypes
    py::bind_vector<std::vector<double>>(m, "VectorDouble");
    py::bind_vector<std::vector<std::vector<double>>>(m, "VectorVectorDouble");

//    Provide module documentation
    m.doc() = "stl_containers plugin: testing conversions"; // optional module docstring

//    void hello_world();
    m.def("hello_world",
          &hello_world,
          "Print hello world");

/**
* @brief Generate a new vector of zeros
* @param size size of the vector
* @return the created vector
*/
//std::vector<double> &getVector(int size);
    m.def("getVector",
          &getVector,
          "Generate a new vector of zeros",
          py::arg("size"),
          py::return_value_policy::take_ownership);


/**
 * @brief Append a number to a vector
 * @param vec the vector in question
 * @param number number in question
 */
//void appendToVector(std::vector<double> &vec, double number);
    m.def("appendToVector",
          &appendToVector,
          "Append a number to a vector",
          py::arg("vec"),
          py::arg("number"));

/**
 * @brief Print a given vector
 * @param vec vector in question
 */
//void printVector(std::vector<double> &vec);
    m.def("printVector",
          &printVector,
          "Print a given vector",
          py::arg("vec"));

/**
 * @brief Generate a new vector of vectors zeros
 * @param size size of the vector
 * @return the created vector
 */
//    std::vector<std::vector<double>> &getVectorOfVectors(int innerSize, int outerSize);
    m.def("getVectorOfVectors",
          &getVectorOfVectors,
          "Generate a new vector of vectors zeros",
          py::arg("innerSize"),
          py::arg("outerSize"),
          py::return_value_policy::take_ownership);

/**
 * @brief Append a number to each of the vectors
 * @param vec the vector in question
 * @param number number in question
 */
//    void appendToEachVector(std::vector<std::vector<double>> &vecOfVecs, double number);
    m.def("appendToEachVector",
          &appendToEachVector,
          "Append a number to each of the vectors",
          py::arg("vecOfVecs"),
          py::arg("number"));

/**
 * @brief Print a given vector of vectors
 * @param vec vector in question
 */
//    void printVectorOfVectors(std::vector<std::vector<double>> &vecOfVecs);
    m.def("printVectorOfVectors",
          &printVectorOfVectors,
          "Print a given vector of vectors",
          py::arg("vecOfVecs"));
}

