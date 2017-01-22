#include <iostream>
#include <string>
#include <cstdio>


void hello_world(){
    std::cout<< "Hello world!\n";
    const char * day = "day!";
    printf("What a beautiful %s\n", day);
    }

int addition(int x, int y){
    return x+y;
    }

void fprint(int x, int y, int (*fcall)(int, int)){
    printf("The values for the function are %i and %i\n", x, y);
    // Call the function normally
    std::cout<<fcall(x, y)<<std::endl;
    // Or dereference it first ot be proper
    std::cout<<(*fcall)(x, y)<<std::endl;
    }

void pass_by_reference(int &i)
{
    std::cout << "acces the value of the variable passed by reference: " << i << std::endl;
    std::cout << std::endl;
}

void pass_by_pointer(int *i)
{
    std::cout << "access the adress of the variable: " << i << std::endl;
    std::cout << "access the value of the variable: " << *i << std::endl;
    std::cout << std::endl;
}

int main(){
    hello_world();
    // A sample variable
    double myvar = 10;
    double myvar2 = 20;

    // Adress of a variable, a separate object that
    // Stores the position in memory of variable myvar

    double * adress_of_myvar = &myvar;
    std::cout<<"The adress of myvar by a pointer is "<<adress_of_myvar<<std::endl;

    // * is the dereferencing operator, given the adress it returns the var
    std::cout<<"The value of myvar by dereference is " << *adress_of_myvar << std::endl;
    std::cout<<"The adress of myvar by ampersand is " << &myvar << std::endl;
    std::cout<<"The adress of myvar by dereferenced ampersand is " << *(&myvar) << std::endl;
    std::cout << std::endl;
    
    // Dereferenced pointre is considered a regular variable 
    printf("The value of myvar is %.0f\n", *adress_of_myvar);
    std::cout << std::endl;

    //It is possible to assign a different variable to a pointer
    adress_of_myvar = &myvar2;
    std::cout << "Switching the adress our pointer is pointing to " << std::endl;

    std::cout<<"The adress of myvar by a pointer is "<<adress_of_myvar<<std::endl;
    std::cout<<"The value of myvar by dereference is " << *adress_of_myvar << std::endl;
    std::cout<<"The adress of myvar by ampersand is " << &myvar2 << std::endl;
    std::cout<<"The adress of myvar by dereferenced ampersand is " << *(&myvar2) << std::endl;
    std::cout << std::endl;

    //Pointers can be used to change values of a variable 
    * adress_of_myvar = 30;
    std::cout << "Switching the value of a variable  " << std::endl;

    std::cout<<"The adress of myvar by a pointer is "<<adress_of_myvar<<std::endl;
    std::cout<<"The value of myvar by dereference is " << *adress_of_myvar << std::endl;
    std::cout<<"The adress of myvar by ampersand is " << &myvar2 << std::endl;
    std::cout<<"The adress of myvar by dereferenced ampersand is " << *(&myvar2) << std::endl;
    std::cout << std::endl;

    // [] acts as a derefrerencing operator, pointing to the following memory blocks
    // i.e. pointer[a] = *(variable)

    std::cout<<"The adress of myvar by a pointer is "<<adress_of_myvar<<std::endl;
    std::cout<<"The value of myvar by dereferenced by [0] is " << adress_of_myvar[0] << std::endl;
    std::cout << std::endl;

    //When the poiter is constant, the value it is poinjting to cannot be modified
    // The pointer itself can be modifies
    const double *p_myvar = &myvar;
    std::cout<<"The value of myvar by dereference is " << *p_myvar << std::endl;
    p_myvar = &myvar2;
    std::cout<<"The value of myvar by dereference is " << *p_myvar << std::endl;
    // *p_myvar = 10    <-- cannot do that
    std::cout << std::endl;


    // Reference to a variable only stores the adress and is automatically dereferenced
    // Sort of like a alias to a variable
    double &reference = myvar;
    std::cout << "The value accessed by the reference is: " << reference << std::endl;


    int testvar = 1;
    //Values can be passed to a function by a pointer - an adress is passed 
    // Since the function is expecting a pointer object 
    pass_by_pointer(&testvar);
    // Or a pointer holding the adress is passed
    int *p_testvar = &testvar;
    pass_by_pointer(p_testvar);

    //And by reference - a reference is passed (autodereferencing)
    pass_by_reference(testvar);


    //Functions can be passed to different functions by reference
    fprint(2, 3, addition);

    
    }
