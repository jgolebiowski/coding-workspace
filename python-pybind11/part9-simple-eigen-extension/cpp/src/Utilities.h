#pragma once

#include "Eigen/Eigen/Dense"
typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> EigenDynamicRowMajor;
typedef Eigen::Ref<EigenDynamicRowMajor> RefEigenDynamicRowMajor;

/**
 * @brief Print Hello world
 */
void hello_world();

/**
 * @brief Print hello world with openMP parallelism
 */
void hello_world_omp();