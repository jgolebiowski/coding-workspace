//
// Created by Golebiowski, Jacek on 6/16/18.
//
#include <Eigen/Dense>
#include <vector>


#ifndef STL_CONTAINERS_VECTOROPERATIONS_H
#define STL_CONTAINERS_VECTOROPERATIONS_H

/**
 * @brief Generate a new Matrix of zeros
 * @param size size of the matrix
 * @return the created vector
 */
Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> &getMatrix(int size);

/**
 * @brief Set matrix elements to random values
 * @param mat the matrix in question
 */
void setRandom(Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> &mat);

/**
 * @brief Print a given matrix
 * @param mat vector in question
 */
void printMatrix(Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> &mat);

/**
 * @brief Get a vector of matrixes of given size
 * @param size Matrix size
 * @param length Vector length
 * @return Created vector
 */
std::vector<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> &getVectorMatrix(
        int size, int length);

/**
 * @brief For every matrix in a vector, matrix elements to random values
 * @param vectorMatrix the vector of matrices in question
 */
void setRandomVectorMatrix(
        std::vector<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> &vectorMatrix);

/**
 * @brief Print the vector of matrices
 * @param vectorMatrix the vector of matrices in question
 */
void printVectorMatrix(
        std::vector<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> &vectorMatrix);


#endif //STL_CONTAINERS_VECTOROPERATIONS_H
