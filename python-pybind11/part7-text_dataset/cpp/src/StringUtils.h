//
// Created by Golebiowski, Jacek on 8/18/18.
//

#ifndef DATASET_UTILS_STRINGUTILS_H
#define DATASET_UTILS_STRINGUTILS_H

#include <string>
#include <vector>

namespace stringUtils
{
    /**
     * @brief Read a file into a string
     * @param filename Name of the file
     * @param contents return: contents of the file, loaded from disk
     */
    void readFile(const std::string &filename, std::string *contents);

    /**
     * @brief Split string into tokens
     * @param s string
     * @param delimiter splitting char
     * @param tokenized return: vector of tokens form the string
     */
    void splitstring(const std::string &s, const std::string &delimiter, std::vector<std::string> *tokenized);

    /**
     * @brief Get all n-grams out of the string
     * @param s string to ngramatize
     * @param n n in ngrams
     * @param ngrams return: fill this vector with ngrams
     */
    void getNGrams(const std::string &s, const size_t &n, std::vector<std::string> *ngrams);

}
#endif //DATASET_UTILS_STRINGUTILS_H

