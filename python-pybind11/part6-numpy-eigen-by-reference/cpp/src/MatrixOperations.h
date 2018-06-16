//
// Created by Golebiowski, Jacek on 6/16/18.
//
#include <Eigen/Dense>
#include <vector>


#ifndef STL_CONTAINERS_VECTOROPERATIONS_H
#define STL_CONTAINERS_VECTOROPERATIONS_H

typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> EigenDynamicRowMajor;
typedef Eigen::Ref<EigenDynamicRowMajor> EigenRefDynamicRowMajor;

/**
 * @brief Generate a new Matrix of zeros
 * @param size size of the matrix
 * @return the created vector
 */
EigenDynamicRowMajor &getMatrix(int size);

/**
 * @brief Set matrix elements to random values
 * @param mat the matrix in question
 */
void setRandom(EigenRefDynamicRowMajor mat);

/**
 * @brief Print a given matrix
 * @param mat vector in question
 */
void printMatrix(EigenRefDynamicRowMajor mat);

/**
 * @brief Get a vector of matrixes of given size
 * @param size Matrix size
 * @param length Vector length
 * @return Created vector
 */
std::vector<EigenRefDynamicRowMajor> &getVectorMatrix(
        int size, int length);

/**
 * @brief For every matrix in a vector, matrix elements to random values
 * @param vectorMatrix the vector of matrices in question
 */
void setRandomVectorMatrix(
        std::vector<EigenRefDynamicRowMajor> &vectorMatrix);

/**
 * @brief Print the vector of matrices
 * @param vectorMatrix the vector of matrices in question
 */
void printVectorMatrix(
        std::vector<EigenRefDynamicRowMajor> &vectorMatrix);


#endif //STL_CONTAINERS_VECTOROPERATIONS_H
