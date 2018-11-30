#pragma once

#include "Eigen/Dense"
typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> EigenMatrixXdRowMajor;

/**
 * @brief Print Hello world
 */
void hello_world();

/**
 * @brief Print hello world with openMP parallelism
 */
void hello_world_omp();