//
// Created by Golebiowski, Jacek on 6/16/18.
//

#include <Example.h>

/**
 * @brief Add two numbers
 * @param i first number
 * @param j second number
 * @return the sum
 */
int add(int i, int j)
{
    return i + j;
}

/**
 * @brief Same as add number but with default arguments
 * @param i first number (def: 1)
 * @param j second number (def: 2)
 * @return sum
 */
int add_default(int i, int j)
{
    return i + j;
}

/**
 * @brief Modify a given string by appending a character at the end
 * @param stringerino string to modify
 * @param toAppend string to append
 */
void appendString(std::string &stringerino, std::string &toAppend)
{
    stringerino.append(toAppend);
}