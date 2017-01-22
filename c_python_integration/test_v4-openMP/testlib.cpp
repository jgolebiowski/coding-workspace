#include <iostream>
#include <cmath>
#include <stdio.h>

extern "C" {


void Hello_world(){
    #pragma omp parallel
        {
        printf("Hello!\n");
        }
    }

void simple_for_loop(int num){
    #pragma omp parallel
        # pragma omp for
            for (int i=0; i<num; i++){
                printf("number %d\n", i);
        }
    }

void ordered_loop(int num){
    #pragma omp parallel for ordered schedule(dynamic)
        for (int i=0; i<num; i++){
            double liczba = exp(i);
            printf("unordered number %d, exp %f\n", i, liczba);
            
            #pragma omp ordered
            printf("number %d, exp %f\n", i, liczba);
        }
    }

void collapsed_loop(int num){
    double sum=0;
    #pragma omp parallel for collapse(2) reduction(+:sum)
    for (int i=0; i<num; i++){
        for (int j=0; j<num; j++){
            sum = sum + i + j;
            }
        }
    printf("total sum: %f\n", sum);
    }

void collapsed_loop_w_atomic(int num){
    double sum=0;
    #pragma omp parallel for collapse(2) shared(sum)
    for (int i=0; i<num; i++){
        for (int j=0; j<num; j++){
            // with atomic clause the event has to be executed completely
            ///and another thread cannot intervene during the execution of the event
            #pragma omp atomic
            sum = sum + i + j;
            }
        }
    printf("total sum: %f\n", sum);
    }

void section_function(int num){
    #pragma omp parallel
        {
        std::cout<<num<<std::endl; 
        }
    }
}


int main(){
    // Set no of cores
    // omp set num threads(4);
    for (int i=0; i<100; i++){
        collapsed_loop(10);
        collapsed_loop_w_atomic(10);
        }

}

