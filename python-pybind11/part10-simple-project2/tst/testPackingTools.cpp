//
// Created by jg2214 on 25/10/18.
//
#include <catch2/catch.hpp>
#include <Eigen/Dense>
#include "Utilities.h"
#include "PackingTools.h"

TEST_CASE("Test get_energy()", "[get_energy]") {

    EigenMatrixXdRowMajor dist;
    double target_energy;
    double output_energy;
    double margin = 1e-2;

    SECTION("First set of numbers to check") {
        dist.resize(10, 1);
        dist << 0.00726564,
                0.34950995,
                0.04929788,
                0.87137316,
                0.17766071,
                0.74177731,
                0.06170628,
                0.77465625,
                0.39984811,
                0.89669267;
        target_energy = 6.8609;

        Approx target = Approx(target_energy).margin(margin);
        output_energy = getEnergy(dist);
        REQUIRE(output_energy == target);
    }

}

TEST_CASE("Test getPlacementEnergy", "[getPlacementEnergy]")
{
    double target_energy;
    double output_energy;
    double margin = 1e-2;

    int natoms = 8;
    int ndims = 3;
    EigenMatrixXdRowMajor system;
    system.resize(natoms, ndims);
    system << 0., 0., 0.,
            0., 0., 1.53219,
            1.04158, 0.05187, -0.36394,
            -0.41137, -0.95846, -0.36365,
            0.41116, 0.95846, 1.89609,
            -1.04173, -0.05201, 1.89583,
            -0.57243, 0.82277, -0.42834,
            0.5721, -0.823, 1.96052;
    EigenMatrixXdRowMajor molecule = system;

    SECTION("FIrst test")
    {
        system.col(0).array() += 3;
        molecule.col(0).array() -= 3;

        target_energy = 0.18;
        Approx target = Approx(target_energy).margin(margin);
        output_energy = getPlacementEnergy(system, molecule);
        REQUIRE(output_energy == target);
    }

    SECTION("Second test")
    {
        system.col(0).array() += 1;
        molecule.col(0).array() -= 1;

        target_energy = 6.37;
        Approx target = Approx(target_energy).margin(margin);
        output_energy = getPlacementEnergy(system, molecule);
        REQUIRE(output_energy == target);
    }

    SECTION("Third test - more atoms")
    {
        EigenMatrixXdRowMajor systemPartA = system;
        EigenMatrixXdRowMajor systemPartB = system;
        systemPartA.col(0).array() += 10;
        systemPartB.col(0).array() += 1;
        system.resize(natoms + natoms, ndims);
        system << systemPartA, systemPartB;

        molecule.col(0).array() -= 1;

        target_energy = 6.37;
        Approx target = Approx(target_energy).margin(margin);
        output_energy = getPlacementEnergy(system, molecule);
        REQUIRE(output_energy == target);
    }
}