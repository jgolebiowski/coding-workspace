"""Main file for the problem"""
from part2.lib import part2

def append_string(str1, str2):
    str1 += str2

def main():
    print(part2.add.__doc__)
    print(part2.add(1, 2))
    print(part2.add(i=1, j=2))

    print(part2.add_default.__doc__)
    print(part2.add_default(i=1))

    print(part2.hello_world_omp.__doc__)
    part2.hello_world_omp()

    # This does not work since strings are immutable in python, see a function
    string1 = "abcs"
    string2 = "elomelo"
    print("Before CPP:", string1)
    part2.appendString(string1, string2)
    print("After CPP:", string1)

    string1 = "abcs"
    string2 = "elomelo"
    print("Before Python:", string1)
    append_string(string1, string2)
    print("After Python:", string1)

if (__name__ == "__main__"):
    main()