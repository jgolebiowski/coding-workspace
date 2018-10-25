//
// Created by Golebiowski, Jacek on 6/16/18.
////
#include <Utilities.h>

#include <pybind11/pybind11.h>


namespace py = pybind11;

// Here, the first argument is the module name which must be the same as cmake project name!!
PYBIND11_MODULE(example_project_cpp, m)
{

//    Provide module documentation
    m.doc() = "Example module: cpp python extension";

/**
 * @brief Print Hello world
 */
//    void hello_world();
    m.def("hello_world",
          &hello_world,
          "Print hello world");

/**
* @brief Print hello world with openMP parallelism
*/
//void hello_world_omp();
    m.def("hello_world_omp",
            &hello_world_omp,
            "Print hello world with openMP parallelism");
}

