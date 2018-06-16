#pragma once

extern "C"
{
/* Define a return tuple structure */
struct myarray
{
    int n_rows;
    int n_cols;
    double * data;
};

/* Initialize a 2dmatrix and return the tuple representation */
myarray myarray_construct(int nRows, int nCols);

} // End of extern C