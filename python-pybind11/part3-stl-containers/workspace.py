"""Main file for the problem"""
from stl_containers.lib import stl_containers


def main():
    print("------ Vector created in CPP")
    stl_containers.hello_world()
    vector_list = stl_containers.getVector(10)
    print(vector_list)

    stl_containers.appendToVector(vector_list, 2.0)
    print(vector_list)

    vector_list.append(4.0)
    stl_containers.printVector(vector_list)

    print("------ Vector created in Python")
    vector_list = [1.0 for item in range(10)]
    print(vector_list)

    stl_containers.appendToVector(vector_list, 2.0)
    print(vector_list)

    vector_list.append(4.0)
    stl_containers.printVector(vector_list)

    print("------ Vector of Vectors created in CPP")
    list_of_lists = stl_containers.getVectorOfVectors(3, 4)
    print("List of lists")
    print(list_of_lists)

    stl_containers.appendToEachVector(list_of_lists, 3.0)
    print("List of lists")
    print(list_of_lists)

    list_of_lists[1].append(5.0)
    stl_containers.printVectorOfVectors(list_of_lists)

    print("------ Vector of Vectors created in Python")
    list_of_lists = [[1.0 for item in range(4)] for item in range(3)]
    print("List of lists")
    print(list_of_lists)

    stl_containers.appendToEachVector(list_of_lists, 3.0)
    print("List of lists")
    print(list_of_lists)

    list_of_lists[1].append(5.0)
    stl_containers.printVectorOfVectors(list_of_lists)


if (__name__ == "__main__"):
    main()
