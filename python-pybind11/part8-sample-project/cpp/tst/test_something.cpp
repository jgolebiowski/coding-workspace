//
// Created by jg2214 on 25/10/18.
//
#include <catch2/catch.hpp>

TEST_CASE("Some example test case", "[example]") {

    int testvar = 2;
    REQUIRE(testvar == 2);

    SECTION("Check if it is still unchanged") {
        REQUIRE(testvar == 2);
    }
}