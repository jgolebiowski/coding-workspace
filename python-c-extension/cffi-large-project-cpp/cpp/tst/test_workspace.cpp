//
// Created by Jacek Golebiowski on 2019-03-13.
//

#include <iostream>
#include <catch2/catch.hpp>
#include "utilities.h"
#include "arraymath.h"

TEST_CASE("Test workspace", "[workspace]")
{
    double a[] = {0.11, 0.12, 0.13,
                  0.21, 0.22, 0.23};

    double b[] = {1011, 1012,
                  1021, 1022,
                  1031, 1032};

    double c[] = {0.00, 0.00,
                  0.00, 0.00};
    arraymath_matmul(a, 2, 3,
                     b, 3, 2,
                     c, 2, 2);
    EigenMap matC(c, 2, 2);
    std::cout << matC << std::endl;


    std::cout << "Hello World!" << std::endl;
    hello_world_omp();
}