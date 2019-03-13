from cpp.extension.utilities import hello_world_omp
from cpp.extension.arraymath import matmul

def main():
    hello_world_omp()
    import ipdb; ipdb.set_trace()

if __name__ == '__main__':
    main()