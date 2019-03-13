//
// Created by jg2214 on 25/10/18.
//
#include <catch2/catch.hpp>
#include "arraymath.h"

TEST_CASE("Test arraymath_matmul", "[arraymath_matmul]")
{
    double margin = 1e-2;
    SECTION("First set of numbers to check")
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

        REQUIRE(c[0] == Approx(367.760000).margin(margin));
        REQUIRE(c[1] == Approx(368.120000).margin(margin));
        REQUIRE(c[2] == Approx(674.060000).margin(margin));
        REQUIRE(c[3] == Approx(674.720000).margin(margin));
    }

}