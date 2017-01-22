#include <iostream>
#include <string>
#include <cstdio>
#include <cstdlib>


void hello_world(){
    std::cout<< "Hello world!\n";
    std::string day = "day!";
    printf("What a beautiful %s\n", day.c_str());
    }

int addition(int x, int y){
    return x+y;
    }


int main(){
    hello_world();
    // A sample variable

    #ifdef __linux
        system("mkdir -p GRD/");
    #endif
    }
