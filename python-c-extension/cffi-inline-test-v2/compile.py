from cffi import FFI


def compile_cffi(project_name, cdef, source):
    """
    Compile the extension using CFFI

    :param project_name: Name of the compilation
    :param cdef: heders for the functions
    :param source: source to compile
    """
    ffibuilder = FFI()
    ffibuilder.cdef(cdef)

    # os.environ["CC"] = "gcc-8"
    # os.environ["CXX"] = "g++-8"
    # CFLAGS = ["-Wall", "-Wextra", "-fdiagnostics-color", "-fopenmp"]
    # INCLUDES = []
    # LIBRARY_DIRS = []
    # LINKER_FLAGS = ["-lm"]

    CFLAGS = ["-Wall", "-Wextra", "-fdiagnostics-color", "-Xpreprocessor", "-fopenmp"]
    INCLUDES = ["-I/usr/local/include"]
    LIBRARY_DIRS = ["-L/usr/local/lib"]
    LINKER_FLAGS = ["-lm", "-liomp5", "-lgsl", "-lcblas"]

    ffibuilder.set_source(project_name,
                          source,
                          extra_compile_args=CFLAGS + INCLUDES,
                          extra_link_args=LIBRARY_DIRS + LINKER_FLAGS,
                          )
    ffibuilder.compile(verbose=True)
