//
// Created by Golebiowski, Jacek on 6/18/18.
//

#include "Base.h"

Base::Base(std::string name) :
        name(name)
{
    std::cout << "Initialized a class: "
              << name
              << std::endl;
}

/**
 * @brief Print the class name and its type
 */
void Base::printName()
{
    std::cout << "This is the Base class called "
              << name
              << std::endl;
}

/**
 * @brief Print a random message
 */
void Base::printMessage()
{
    std::cout << "Secret message from the Base class!"
              << std::endl;
}

/**
 * @brief Print a second random message
 */
void Base::printSecondMessage()
{
    std::cout << "Second Secret message from the Base class!"
              << std::endl;
}