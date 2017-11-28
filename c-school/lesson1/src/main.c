/* Hello World program */
#include <stdio.h>

#include "UtilityFunctions.h"
#include "MyarrayCore.h"
#include "MyarrayMath.h"

int main()
{
    myHelloworld();
    const int N = 3;
    struct myarray * A = myarray_construct(N, N);
    struct myarray * B = myarray_construct(N, N);

    myarray_arange(A);
    myarray_arange(B);

    struct myarray *C = myarray_matmul(A, B);
    myarray_add(B, A);

    myarray_print(A);
    myarray_print(B);
    myarray_print(C);

    myarray_destroy(A);
    myarray_destroy(B);
    myarray_destroy(C);

/*    struct myarray * new_array = myarray_construct(3, 3);
    printf("Address of element 0, 1 is %p\n", myarray_at(new_array, 0, 1));
    printf("Value of element 0, 1 is %f\n", myarray_value_at(new_array, 0, 1));
    myarray_print(new_array);
    * myarray_at(new_array, 0, 1) = 10;
    printf("Address of element 0, 1 after change is %p\n", myarray_at(new_array, 0, 1));
    myarray_print(new_array);

    myarray_zero(new_array);
    myarray_print(new_array);

    myarray_destroy(new_array);*/
    return 0;

}