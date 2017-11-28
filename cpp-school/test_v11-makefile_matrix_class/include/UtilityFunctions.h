#pragma once

extern "C"
{

void hello_world();
void square_array(double * data_array, int nrows, int ncols);
void square_matrix(double * data_array, int nrows, int ncols);
void square_mymatrix(MyMatrix & data_mymatrix);

} // End of extern C