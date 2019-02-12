//
// Created by Jacek Golebiowski on 2019-02-12.
//
#include "minunit.h"

#include <gsl/gsl_matrix.h>
#include "utilities.h"
#include "arraymath.h"
#include "stdio.h"

MU_TEST(test_simple_matmul)
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


//    gsl_matrix_view RES = gsl_matrix_view_array(c, 2, 2);
//    gsl_matrix_fprintf(stdout, &RES.matrix, "%f");

    mu_assert_double_eq(c[0], 367.760000);
    mu_assert_double_eq(c[1], 368.120000);
    mu_assert_double_eq(c[2], 674.060000);
    mu_assert_double_eq(c[3], 674.720000);
}

MU_TEST_SUITE(test_arraymath)
{

    MU_RUN_TEST(test_simple_matmul);
}


