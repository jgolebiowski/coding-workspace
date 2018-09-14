//
// Created by Golebiowski, Jacek on 6/16/18.
////
#include <Utilities.h>

#include <Eigen/Dense>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/eigen.h>


namespace py = pybind11;

// Here, the first argument is the module name which must be the same as cmake project name!!
PYBIND11_MODULE(dataset_utils, m)
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
}

