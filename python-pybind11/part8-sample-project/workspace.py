"""Main file for the problem"""
import numpy as np
from example_project.clib import example_project_cpp

def main():
    example_project_cpp.hello_world_omp()


if (__name__ == "__main__"):
    main()
