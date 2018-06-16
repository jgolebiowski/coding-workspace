//
// Created by Golebiowski, Jacek on 6/16/18.
//
#include <vector>

#ifndef STL_CONTAINERS_VECTOROPERATIONS_H
#define STL_CONTAINERS_VECTOROPERATIONS_H

/**
 * @brief Generate a new vector of zeros
 * @param size size of the vector
 * @return the created vector
 */
std::vector<double> &getVector(int size);

/**
 * @brief Append a number to a vector
 * @param vec the vector in question
 * @param number number in question
 */
void appendToVector(std::vector<double> &vec, double number);

/**
 * @brief Print a given vector
 * @param vec vector in question
 */
void printVector(std::vector<double> &vec);

/**
 * @brief Generate a new vector of vectors zeros
 * @param size size of the vector
 * @return the created vector
 */
std::vector<std::vector<double>> &getVectorOfVectors(int innerSize, int outerSize);

/**
 * @brief Append a number to each of the vectors
 * @param vec the vector in question
 * @param number number in question
 */
void appendToEachVector(std::vector<std::vector<double>> &vecOfVecs, double number);

/**
 * @brief Print a given vector of vectors
 * @param vec vector in question
 */
void printVectorOfVectors(std::vector<std::vector<double>> &vecOfVecs);

#endif //STL_CONTAINERS_VECTOROPERATIONS_H
