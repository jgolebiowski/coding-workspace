/* My array math source */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <omp.h>

#include "MyarrayCore.h"
#include "MyarrayMath.h"

/*Multiply the first array by the second one element wise
Think of A *= B*/
void myarray_multiply_elwise(struct myarray * A, struct myarray * B)
{
    int i, j;
    assert(A->n_rows == B->n_rows);
    assert(A->n_cols == B->n_cols);

    #pragma omp parallel for schedule(static) collapse(2)\
            private(i, j) shared(A, B) default(none)
    for (i = 0; i < A->n_rows; i++)
    for (j = 0; j < A->n_cols; j++)
    {
        *myarray_at(A, i, j) *= (*myarray_at(B, i, j));
    }
}

/*Add the arrays in place, Think of A += B*/
void myarray_add(struct myarray * A, struct myarray * B)
{
    int i, j;
    assert(A->n_rows == B->n_rows);
    assert(A->n_cols == B->n_cols);

    #pragma omp parallel for schedule(static) collapse(2)\
            private(i, j) shared(A, B) default(none)
    for (i = 0; i < A->n_rows; i++)
    for (j = 0; j < A->n_cols; j++)
    {
        *myarray_at(A, i, j) += (*myarray_at(B, i, j));
    }
}

/*Multiply two arrays together and return the result*/
struct myarray * myarray_matmul(struct myarray * A, struct myarray * B)
{
    int i, j, k;
    const int n = A->n_rows;
    const int mA = A->n_cols;
    const int mB = B->n_rows;
    const int p = B->n_cols;
    struct myarray * C;

    assert(mA == mB);
    C = myarray_construct(n, p);

    #pragma omp parallel for schedule(static) collapse(2)\
            private(i, j, k) shared(A, B, C) default(none)
    for (i = 0; i < n; i++)
    for (j = 0; j < p; j++)
    {
        *myarray_at(C, i, j) = 0;
        /* calculate an element */
        for (k = 0; k < mA; k++)
        {
            *myarray_at(C, i, j) += *myarray_at(A, i, k) * (*myarray_at(B, k, j));
        }
    }

    return C;

}