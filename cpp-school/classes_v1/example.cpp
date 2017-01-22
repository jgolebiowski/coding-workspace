#include <iostream>
#include <string>
#include <cstdio>


void hello_world(){
    std::cout<< "Hello world!\n";
    const char * day = "day!";
    printf("What a beautiful %s\n", day);
    }

class Rectangle{

    // two data entries with private access
    double width;
    double height;

    public:
        // Constructor of the rectangle object
        Rectangle(double, double);
        //The constructor can be overloaded to add a default constructor
        // In this case the default constr jus tcreates an ampty object
        Rectangle (){
            //do nothing  - create an empty object
            }
        //two functions with public access
        void set_values(double, double);  
        double area(){
            return width * height;
            }
    }myrectangle;

class Vector{
    public:
        //variables
        double x, y, z;

        //constructors
        Vector() { /* pass */};
        Vector(double inx, double iny, double inz){
            x = inx;
            y = iny;
            z = inz;
            }
        //Destructor
        ~Vector(){
            // Free any allocated memory
            }

        //functions
        double lenghtsq (void);

        //overloaded operator
        Vector operator + (const Vector &param);
    };

double Vector::lenghtsq(){
    return double(x*x + y*y + z*z);
    }

Vector Vector::operator+ (const Vector &param){
    Vector temp;
    temp.x = x + param.x;
    temp.y = y + param.y;
    temp.z = z + param.z;
    return temp;
    }

void Rectangle::set_values(double x, double y){
    width = x;
    height = y;
    }

// Definition of the rectangle constructor
Rectangle::Rectangle(double x, double y){
    width = x;
    height = y;
    }


int main(){
    hello_world();

    Vector myvecta (1, 2, 4);
    Vector myvectb (2, 4, 5);
    Vector myvectc;

    myvectc = myvecta + myvectb;
    printf("The vale of added vector is (%.0f, %.0f, %.0f)\n", myvectc.x, myvectc.y, myvectc.z);

    myrectangle.set_values(10, 20);
    printf("The area of the rectangle is %.0f\n", myrectangle.area());

    Rectangle myrekt;
    myrekt.set_values(5,20);
    printf("The area of the rect is %.0f\n", myrekt.area());

    Rectangle con_rekt (10, 30);
    printf("The area of the con_rect is %.0f\n", con_rekt.area());
    }
