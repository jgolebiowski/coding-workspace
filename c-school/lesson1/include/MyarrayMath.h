/* My array math  headers */
#pragma once
#include <stdio.h>
#include <stdlib.h>

#include "MyarrayCore.h"

/*Multiply the first array by the second one element wise
Think of A *= B*/
void myarray_multiply_elwise(struct myarray * A, struct myarray * B);

/*Add the arrays in place, Think of A += B*/
void myarray_add(struct myarray * A, struct myarray * B);

/*Multiply two arrays together and return the result*/
struct myarray * myarray_matmul(struct myarray * A, struct myarray * B);