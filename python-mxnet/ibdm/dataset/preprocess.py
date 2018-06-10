"""Tools ot load in and pre-process the dataset"""
import os

def main():
    level0 = ["train", "test"]
    level1 = ["pos", "neg"]
    list_of_entries = []
    for l0 in level0:
        for l1 in level1:
            for element in os.listdir(os.path.join("aclImdb", l0, l1)):
                list_of_entries.append((l0, l1, element))

    print(len(list_of_entries))



if (__name__ == "__main__"):
    main()