#include <iostream>
#include <iostream>
#include <string>
#include <Utilities.h>
#include <Example.h>

int main()
{
    hello_world();
    hello_world_omp();
    std::string str1 = "abcds";
    std::string str2 = "eloelo";
    std::cout << "String before function call: "
              << str1
              << std::endl;

    appendString(str1, str2);

    std::cout << "String after function call: "
              << str1
              << std::endl;


}