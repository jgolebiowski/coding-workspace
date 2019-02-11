from ._project_extension import lib 

def hello_world():
    """
    Print Hello world!
    """
    lib.hello_world()

def hello_world_omp():
    """
    Print hello world with openMP parallelism
    """
    lib.hello_world_omp()