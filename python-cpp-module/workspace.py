"""Main file for the problem"""

from integration_tools.extensions.utilities import hello_world, hello_world_omp
from integration_tools.extensions.interface import get_vector

def main():
    print("Calling cpp")
    hello_world()
    hello_world_omp()
    print(get_vector(3))

if (__name__ == "__main__"):
    main()