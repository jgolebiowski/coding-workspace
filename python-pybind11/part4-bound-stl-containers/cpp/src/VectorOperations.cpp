//
// Created by Golebiowski, Jacek on 6/16/18.
//
#include <vector>
#include <VectorOperations.h>
#include <iostream>


/**
 * @brief Generate a new vector of zeros
 * @param size size of the vector
 * @return the created vector
 */
std::vector<double> &getVector(int size)
{
    auto vec = new std::vector<double>(size, 0);
    return *vec;
}

/**
 * @brief Append a number to a vector
 * @param vec the vector in question
 * @param number number in question
 */
void appendToVector(std::vector<double> &vec, double number)
{
    vec.push_back(number);
}

/**
 * @brief Print a given vector
 * @param vec vector in question
 */
void printVector(std::vector<double> &vec)
{
    std::cout << "CppVector: [";
    for (double &element : vec)
    {
        std::cout << element << ", ";
    }
    std::cout << "]"
              << std::endl;
}

/**
 * @brief Generate a new vector of vectors zeros
 * @param size size of the vector
 * @return the created vector
 */
std::vector<std::vector<double>> &getVectorOfVectors(int innerSize, int outerSize)
{
    auto vectorOfVectors = new std::vector<std::vector<double>>;
    for (int i = 0; i < outerSize; i++)
    {
        auto innerVector = new std::vector<double>(innerSize, 0);
        vectorOfVectors->push_back(*innerVector);
    }
    return *vectorOfVectors;
}

/**
 * @brief Append a number to each of the vectors
 * @param vec the vector in question
 * @param number number in question
 */
void appendToEachVector(std::vector<std::vector<double>> &vecOfVecs, double number)
{
    for (std::vector<double> &element : vecOfVecs)
    {
        element.push_back(number);
    }
}

/**
 * @brief Print a given vector of vectors
 * @param vec vector in question
 */
void printVectorOfVectors(std::vector<std::vector<double>> &vecOfVecs)
{
    std::cout << "Vector of vectors:" << std::endl;
    for (std::vector<double> &element : vecOfVecs)
    {
        printVector(element);
    }
}