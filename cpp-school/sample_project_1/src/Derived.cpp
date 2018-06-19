//
// Created by Golebiowski, Jacek on 6/18/18.
//

#include "Derived.h"
#include <Base.h>
#include <string>

Derived::Derived(std::string name) :
        Base(name)
{
    std::cout << "Initialized a Derived class with a call to the Base class, the name is: "
              << name
              << std::endl;
}

/**
 * @brief Print the class name and its type
 */
void Derived::printName()
{
    std::cout << "This is the Derived class called "
              << name
              << std::endl;
}



/**
 * @brief Print a second random message
 */
void Derived::printSecondMessage()
{
    std::cout << "Second Secret message from the Derived class class!"
              << std::endl;
}