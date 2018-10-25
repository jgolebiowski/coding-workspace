#include <iostream>
#include <Utilities.h>

// Let Catch provide main():
#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>

TEST_CASE("All test cases reside in other .cpp files (empty)", "[test_main]") {
    hello_world();
}