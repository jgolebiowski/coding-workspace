#include <iostream>
#include <Utilities.h>
#include <PackingTools.h>
#include "Eigen/Dense"

int main()
{
    hello_world();
    EigenMatrixXdRowMajor system;
    double target_energy;
    double output_energy;

    system.resize(8, 3);
    system << 0., 0., 0.,
            0., 0., 1.53219,
            1.04158, 0.05187, -0.36394,
            -0.41137, -0.95846, -0.36365,
            0.41116, 0.95846, 1.89609,
            -1.04173, -0.05201, 1.89583,
            -0.57243, 0.82277, -0.42834,
            0.5721, -0.823, 1.96052;
    EigenMatrixXdRowMajor molecule = system;
    molecule.col(0).array() += 3;
    system.col(0).array() -= 3;

    target_energy = 6.8609;
    output_energy = getPlacementEnergy(system, molecule);

    std::cout << "target_energy:" << std::endl << target_energy << std::endl
              << "output_energy:" << std::endl << output_energy << std::endl;
}
