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

    for (i = 0; i < A->n_rows; i++)
    {
        for (j = 0; j < A->n_cols; j++)
        {
            *myarray_at(A, i, j) *= (*myarray_at(B, i, j));
        }
    }
}