import os

from cffi import FFI
from typing import List


def compile_cffi(project_name: str, cdef: str, extra_header: str, source_files: List[str]):
    """
    Compile the extension using CFFI

    :param project_name: Name of the compiled project
    :param cdef: heders for the functions
    :param extra_header: Extra header definition to add to the generated c file
    :param source_files: List of source file names
    """
    ffibuilder = FFI()
    ffibuilder.cdef(cdef)

    os.environ["CC"] = "g++-8"
    os.environ["CXX"] = "g++-8"

    CFLAGS = ["-std=c++11", "-Wall", "-Wextra","-fdiagnostics-color", "-fopenmp"]
    INCLUDES = ["-I/usr/local/include"]

    LINKER_FLAGS = ["-lm", "-fopenmp", "-liomp5"]
    LIBRARY_DIRS = ["-L/usr/local/lib"]

    ffibuilder.set_source(project_name,
                          extra_header,
                          sources=source_files,
                          extra_compile_args=CFLAGS + INCLUDES,
                          extra_link_args=LIBRARY_DIRS + LINKER_FLAGS,
                          )
    ffibuilder.compile(verbose=True)
