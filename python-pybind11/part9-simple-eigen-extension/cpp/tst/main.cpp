#include <iostream>
#include <Utilities.h>
#include <PackingTools.h>
#include "Eigen/Eigen/Dense"

int main() {
    hello_world();
    EigenDynamicRowMajor m = EigenDynamicRowMajor::Random(3,3);
    get_energy(m);
}
