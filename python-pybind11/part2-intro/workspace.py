"""Main file for the problem"""
from part2.lib import part2


def main():
    print(part2.add.__doc__)
    print(part2.add(1, 2))
    print(part2.add(i=1, j=2))

    print(part2.add_default.__doc__)
    print(part2.add_default(i=1))

    print(part2.hello_world_omp.__doc__)
    print(part2.hello_world_omp())

if (__name__ == "__main__"):
    main()