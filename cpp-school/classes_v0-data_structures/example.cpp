#include <iostream>
#include <string>
#include <cstdio>


void hello_world(){
        std::cout<< "Hello world!\n";
}

struct car {
    const char * make;
    int price;
    double milage;
} alfa;

void printcar(car samplecar){
    printf("Your car is made by %s\n", samplecar.make);
    printf("It cost %i £\n", samplecar.price);
    printf("It has driven %.2f miles\n", samplecar.milage);
    }

void printgarage(car garage[], int size){
    for (int i = 0; i<size; i++){
        printcar(garage[i]);
        }
    }

int main(){
    hello_world();
    
    // Defined in code
    car frelek;
    frelek.make = "Land Rover";
    frelek.price = 20000;
    frelek.milage = 100000;
    printcar(frelek);

    // Defined at struct creation
    alfa.make = "Alfa Romeo";
    alfa.price = 18000;
    alfa.milage = 300000;
    printcar(alfa);

    // Array of struct objects
    car garage[2];
    garage[0] = frelek;
    garage[1] = alfa;

    printf("\nThe garage is as follows:\n");
    printgarage(garage, 2);

    //------ Pointer to a structure
    //This is a pointer to a structure blyskawica
    car * pblyskawica;
    // Need to first declare a structure it is pointing to
    // Either by malloc(sizeof(car)) or just by declaring one 
    car ablyskawica;
    pblyskawica = &(ablyskawica);
    
    // Dereferencing operator a->b
    // Member b of an object poinbted to by a, equivalent of (*a).b

    pblyskawica->make = "Jaguar";
    pblyskawica->price = 100000;
    pblyskawica->milage = 40000;

    printf("\n");
    printcar(ablyskawica);
    }
