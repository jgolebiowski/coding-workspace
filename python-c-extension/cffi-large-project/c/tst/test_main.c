//
// Created by Jacek Golebiowski on 2019-02-12.
//
#include "minunit.h"
#include "test_arraymath.h"

int main()
{
    MU_RUN_SUITE(test_arraymath);
    MU_REPORT();
    return 0;
}
