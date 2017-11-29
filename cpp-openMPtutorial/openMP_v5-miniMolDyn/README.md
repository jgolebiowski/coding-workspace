# miniMolDyn
Simple Molecular Dynamics code with openMP parallelisation

The program is quite a basic one, with a lot of room for improvement.
The general structure is based on ASE (Atomistic Simulation Library):

Atoms: object responsible for holding the information about the structure
    Currently only supports single elements

LJCalculator: object responsible for calculating the forces
    Uses a simple Lennard-Jones potential

Dynamics: object responsible for evolving the sytem in time
    have multiple functions for step(), each using a different type of 
    parallelisation