/* My array core  headers */
#pragma once
#include <stdio.h>
#include <stdlib.h>

struct myarray 
{
    int n_rows;
    int n_cols;
    double * data;
};


/* Constructur for myarray */
struct myarray * myarray_construct(int nRows, int nCols);

/* Destructor for Myarray */
void myarray_destroy(struct myarray * self);

/* Access an element of myarray */
double * myarray_at(struct myarray * self, int i, int j);

/* Return a value of (i, j) element of myarray */
double myarray_value_at(struct myarray * self, int i, int j);

/* Print an array */
void myarray_print(struct myarray * self);

/* Zero an array */
void myarray_zero(struct myarray * self);

/* Assign increasing numbers to an array */
void myarray_arange(struct myarray * self);