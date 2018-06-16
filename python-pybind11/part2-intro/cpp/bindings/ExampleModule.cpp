//
// Created by Golebiowski, Jacek on 6/16/18.
////
#include <Example.h>
#include <Utilities.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

// Here, the first argument is the module name which must be the same as cmake project name!!
PYBIND11_MODULE(part2, m)
{
    m.doc() = "pybind11 example plugin"; // optional module docstring

//    int add(int i, int j);
    m.def("add",
          &add,
          "A function which adds two numbers",
          py::arg("i"), py::arg("j"));

//    int add_default(int i = 1, int j=2);
    m.def("add_default",
          &add_default,
          "A function which adds two numbers with default arguments",
          py::arg("i") = 1, py::arg("j") = 2);

//    void hello_world_omp();
    m.def("hello_world_omp",
          &hello_world_omp,
          "Print hello world with openMP parallelism");
}

