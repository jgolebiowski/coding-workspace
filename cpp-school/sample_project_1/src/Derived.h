//
// Created by Golebiowski, Jacek on 6/18/18.
//

#include <Base.h>
#include <string>

#ifndef SAMPLE_PROJECT_DERIVED_H
#define SAMPLE_PROJECT_DERIVED_H


class Derived : public Base
{

public:
    /**
     * @brief Specify default constructor and destructor
     */
    Derived()= default;
    ~Derived()= default;

    /**
     * @brief Constructor
     * @param name the name of this class
     */
    Derived(std::string name);

    /**
     * @brief Print the class name and its type
     */
    void printName() override;


    /**
     * @brief Print a second random message
     */
    void printSecondMessage();

};


#endif //SAMPLE_PROJECT_DERIVED_H
