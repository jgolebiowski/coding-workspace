/* My array core source */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <omp.h>

#include "MyarrayCore.h"

/* Constructur for myarray */
struct myarray * myarray_construct(int nRows, int nCols)
{
    /* Create the structure and data */
    struct myarray * self;
    double * data;

    /* Allocate the memory for structure */
    self = malloc(sizeof(struct myarray));
    if (self)
    {
        /* Fill it with Data */
        self->n_rows = nRows;
        self->n_cols = nCols;
        data = malloc(nRows * nCols * sizeof(double));
        self->data = data;
    }

    return self;
}

/* Destructor for Myarray */
void myarray_destroy(struct myarray * self)
{
    /* Free the data then free the structure */
    free(self->data);
    free(self);
}

/* Return a pointer to (i, j) element of myarray */
double * myarray_at(struct myarray * self, int i, int j)
{
    assert(i >= 0 && i < self->n_rows);
    assert(j >= 0 && j < self->n_cols);
    return &self->data[i * self->n_cols + j];
}

/* Return a value of (i, j) element of myarray */
double myarray_value_at(struct myarray * self, int i, int j)
{
    assert(i >= 0 && i < self->n_rows);
    assert(j >= 0 && j < self->n_cols);
    return self->data[i * self->n_cols + j];
}

/* Print a myarray */
void myarray_print(struct myarray * self)
{
    int i, j;
    printf("This is myarray:\n");
    for (i = 0; i < self->n_rows; i++)
    {
        for (j = 0; j < self->n_cols; j++)
        {
            printf("%-9.3f ", *myarray_at(self, i, j));
        }
        printf("\n");
    }
}

/* Zero an array */
void myarray_zero(struct myarray * self)
{
    int i, j;
    for (i = 0; i < self->n_rows; i++)
    for (j = 0; j < self->n_cols; j++)
    {
        *myarray_at(self, i, j) = 0;
    }
}

/* Assign increasing numbers to an array */
void myarray_arange(struct myarray * self)
{
    int i, j;
    for (i = 0; i < self->n_rows; i++)
    for (j = 0; j < self->n_cols; j++)
    {
        *myarray_at(self, i, j) = i * self->n_cols + j; 
    }
}
