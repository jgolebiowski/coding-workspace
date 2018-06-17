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
          "/**\n"
          " * @brief Add two numbers\n"
          " * @param i first number\n"
          " * @param j second number\n"
          " * @return the sum\n"
          " */",
          py::arg("i"), py::arg("j"));

//    int add_default(int i = 1, int j=2);
    m.def("add_default",
          &add_default,
          "/**\n"
          " * @brief Add two number with default arguments\n"
          " * @param i first number (def: 1)\n"
          " * @param j second number (def: 2)\n"
          " * @return sum\n"
          " */",
          py::arg("i") = 1, py::arg("j") = 2);

    /**
 * @brief Modify a given string by appending a character at the end
 * @param stringerino string to modify
 * @param toAppend string to append
 */
//    void appendString(std::string &stringerino, std::string &toAppend)
    m.def("appendString",
          &appendString,
          " * @brief Modify a given string by appending a character at the end\n"
          " * @param stringerino string to modify\n"
          " * @param toAppend string to append",
          py::arg("stringerino"),
          py::arg("toAppend"));

//    void hello_world_omp();
    m.def("hello_world_omp",
          &hello_world_omp,
          "Print hello world with openMP parallelism");
}

