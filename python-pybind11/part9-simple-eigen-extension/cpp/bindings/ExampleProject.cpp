//
// Created by Golebiowski, Jacek on 6/16/18.
////
#include <Utilities.h>

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <PackingTools.h>


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

/**
 * Get placement energy from atomic positions
 *
 * @param systemPositions positions of the system atoms as (n_sys_atoms, 3) matrix
 * @param moleculePositions positions of the molecule atoms as (n_mol_atoms, 3) matrix
 * @return This will be populated with the total energy
 */
//    double getPlacementEnergy(const Eigen::Ref<EigenMatrixXdRowMajor> systemPositions,
//                              const Eigen::Ref<EigenMatrixXdRowMajor> moleculePositions);
    m.def("getPlacementEnergy",
            &getPlacementEnergy,
            "* Get placement energy from atomic positions\n"
            "*\n"
            "* @param systemPositions positions of the system atoms as (n_sys_atoms, 3) matrix\n"
            "* @param moleculePositions positions of the molecule atoms as (n_mol_atoms, 3) matrix\n"
            "* @param energy This will be populated with the total energy",
            py::arg("systemPositions").noconvert(),
            py::arg("moleculePositions").noconvert());
}

