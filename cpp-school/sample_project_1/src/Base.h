//
// Created by Golebiowski, Jacek on 6/18/18.
//

#include <iostream>
#include <string>

#ifndef SAMPLE_PROJECT_BASE_H
#define SAMPLE_PROJECT_BASE_H


class Base
{
protected:
    std::string name;

public:
    /**
     * @brief Specify default constructor and destructor
     */
    Base()= default;
    ~Base()= default;

    /**
     * @brief Constructor
     * @param name the name of this class
     */
    Base(std::string name);

    /**
     * @brief Print the class name and its type
     */
    virtual void printName();

    /**
     * @brief Print a random message
     */
    virtual void printMessage();

    /**
     * @brief Print a second random message
     */
    void printSecondMessage();

};


#endif //SAMPLE_PROJECT_BASE_H
