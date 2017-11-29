#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <omp.h>

#include <Eigen/Dense>
#include <Atoms.h>
#include <LJCalculator.h>
#include <Dynamics.h>

//Standard constructor
Dynamics::Dynamics(Atoms *simAtoms, LJCalculator * simCalculator, double timeStepperino, std::string fileNAme)
{
    this->atoms = simAtoms;
    this->calculator = simCalculator;
    this->timeStep = timeStepperino;
    this->nSteps = 0;
    this->trajName = fileNAme;

    this->accelerations = Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>::Constant(simAtoms->nAtoms, simAtoms->nDim, 0);
}

//Empty constructor just in case
Dynamics::Dynamics(){}

//Destructor, so far not neede
// ~Dynamics();

// Initialize dynamics
void Dynamics::Initialize()
{
    //pass
}


// Run the dynamics
void Dynamics::run(int nSteps)
{
    #pragma omp parallel default(shared)
    {
        for (int i = 0; i < nSteps; i++)
        {
            this->stepOMPorphan();
    
        }
    }
}

// Perform one MD step
void Dynamics::step()
{
    // calculate accelerationss
    calculator->calculate(atoms);
    accelerations = atoms->forces;

    for (int i = 0; i < atoms->nAtoms; i++)
    {
        // Update velocities
        atoms->velocities.row(i).array() += accelerations.row(i).array();
        // Update positions
        atoms->positions.row(i).array() += atoms->velocities.row(i).array() * timeStep;
    }

    // Update atomic energies
    atoms->potEne = atoms->energies.sum();
    atoms->kinEne = atoms->velocities.squaredNorm() / 2;

    //Print values
    this->printThermoStatus();

    //Write trajectory
    this->atoms->printAtomsXYZ(trajName);

    //Increase nSteps
    this->nSteps++;
}

void Dynamics::stepOMPorphan()
{
        
    // calculate accelerationss
    calculator->calculate(atoms);

    // This could be vectorized to leverage Eigen parallelism instead of parallelizng by openMP
    // using the library is the point of this excercise though.
    #pragma omp for schedule(static)
    for (int i = 0; i < atoms->nAtoms; i++)
    {
        //Update accelerations
        accelerations.row(i) = atoms->forces.row(i);
        // Update velocities
        atoms->velocities.row(i).array() += accelerations.row(i).array();
        // Update positions
        atoms->positions.row(i).array() += atoms->velocities.row(i).array() * timeStep;
    }

    #pragma omp single
    {
        // Update atomic energies
        atoms->potEne = atoms->energies.sum();
        atoms->kinEne = atoms->velocities.squaredNorm() / 2;
    
        //Print values
        this->printThermoStatus();
    
        //Write trajectory
        // this->atoms->printAtomsXYZ(trajName);
    
        //Increase nSteps
        this->nSteps++;
    }
}


// Perform one MD step
void Dynamics::stepOMP()
{
        
    #pragma omp parallel default(none) \
            shared(calculator, atoms, timeStep)
    {
        // calculate accelerationss
        calculator->calculate(atoms);

        // This could be vectorized to leverage Eigen parallelism instead of parallelizng by openMP
        // using the library is the point of this excercise though.
        #pragma omp for schedule(static)
        for (int i = 0; i < atoms->nAtoms; i++)
        {
            //Update accelerations
            accelerations.row(i) = atoms->forces.row(i);
            // Update velocities
            atoms->velocities.row(i).array() += accelerations.row(i).array();
            // Update positions
            atoms->positions.row(i).array() += atoms->velocities.row(i).array() * timeStep;
        }
    }

    // Update atomic energies
    atoms->potEne = atoms->energies.sum();
    atoms->kinEne = atoms->velocities.squaredNorm() / 2;

    //Print values
    this->printThermoStatus();

    //Write trajectory
    // this->atoms->printAtomsXYZ(trajName);

    //Increase nSteps
    this->nSteps++;
}

//print thermo status
void Dynamics::printThermoStatus()
{
    if (nSteps == 0)
    {
        std::cout << "nSteps    kinEne      potEne" << std::endl;
    }
    std::cout << nSteps << "    "
              << atoms->kinEne << "     "
              << atoms->potEne << std::endl;
}
