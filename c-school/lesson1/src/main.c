/* Hello World program */
#include <stdio.h>

#include "UtilityFunctions.h"
#include "MyarrayCore.h"
#include "MyarrayMath.h"

int main()
{
    int i;
    myHelloworld();
    const int N = 3;
    struct myarray * new_array = myarray_construct(N, N);
    struct myarray * new_array2 = myarray_construct(N, N);

    myarray_arange(new_array);
    myarray_arange(new_array2);

    myarray_print(new_array);
    myarray_multiply_elwise(new_array, new_array2);
    myarray_print(new_array);

    myarray_destroy(new_array);
    myarray_destroy(new_array2);

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