"""Main file for the problem"""

from part1.utilities import hello_world, hello_world_omp
from part1.interface import get_vector

def main():
    print("Calling cpp")
    hello_world()
    hello_world_omp()
    print(get_vector(3))

if (__name__ == "__main__"):
    main()