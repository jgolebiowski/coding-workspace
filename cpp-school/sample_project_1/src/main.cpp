#include <iostream>
#include <Utilities.h>
#include <Base.h>
#include <Derived.h>
#include <Logger.h>

int main()
{
    auto sink_cout = std::make_shared<AixLog::SinkCout>(AixLog::Severity::trace, AixLog::Type::normal);
    auto sink_file = std::make_shared<AixLog::SinkFile>(AixLog::Severity::trace, AixLog::Type::all, "logfile.txt");
    AixLog::Log::init({sink_cout, sink_file});

    helloWorld();
    int i = 1;
    std::cout << "Original number " << i << std::endl;

    int &refI = i;
    std::cout << "Reference to a number " << refI << std::endl;

    refI += 1;
    std::cout << "Reference to a number " << refI << std::endl;
    std::cout << "Original number " << i << std::endl;

    int a = 10;
    std::cout << "Original number " << a << std::endl;

    int *ptrA = &a;
    std::cout << "Pointer to a number " << *ptrA << std::endl;
    std::cout << "Address of a pointer to a number " << ptrA << std::endl;

    *ptrA += 1;
    std::cout << "Original number " << a << std::endl;
    std::cout << "Pointer to a number " << *ptrA << std::endl;

    std::cout << std::endl;
    Base *baseClass = new Base("BaseClasserino");
    baseClass->printName();
    baseClass->printMessage();
    baseClass->printSecondMessage();

    std::cout << std::endl;
    Base *derivedClass = new Derived("DerivedClasserino");
    derivedClass->printName();
    derivedClass->printMessage();
    derivedClass->printSecondMessage();

    std::cout << std::endl;
    Derived derivedClassObject("DerivedClasserino");
    derivedClassObject.printName();
    derivedClassObject.printMessage();
    derivedClassObject.printSecondMessage();
}