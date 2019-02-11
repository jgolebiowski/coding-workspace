import shutil

from cffi import FFI
import os

WORKDIR = os.path.dirname(os.path.realpath(__file__))
C_PROJECT_NAME = "_project_extension"
EXTENSION_DIR = "extension"
C_HEADER = """

///////////////////////////////////////////////////////////////////////////////
// utilities.h
///////////////////////////////////////////////////////////////////////////////
/* Print hello world */
void hello_world(void);

/* Print hello world with openMP parallelism */
void hello_world_omp(void);

///////////////////////////////////////////////////////////////////////////////
// arraymath.h
///////////////////////////////////////////////////////////////////////////////
/**
 * This function assigns matRES = matA @ matB
 * @param matA Data for the input matrix
 * @param matAcols Dimensions for the input matrix
 * @param matArows Dimensions for the input matrix
 * @param matB Data for the input matrix
 * @param matBcols Dimensions for the input matrix
 * @param matBrows Dimensions for the input matrix
 * @param matRES Data for the output matrix
 * @param matREScols Dimensions for the output matrix
 * @param matRESrows Dimensions for the output matrix
 */
void arraymath_matmul(
        double *matA, int matAcols, int matArows,
        double *matB, int matBcols, int matBrows,
        double *matRES, int matREScols, int matRESrows);
"""


def compile_cffi():
    """
    Compile the extension using CFFI
    """
    ffibuilder = FFI()
    ffibuilder.cdef(C_HEADER)

    output_c_extension_name = C_PROJECT_NAME

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

    SRCDIR = "src"
    sources = [os.path.join(SRCDIR, file) for file in os.listdir(SRCDIR) if file.endswith(".c")]
    headers = [os.path.join(SRCDIR, file) for file in os.listdir(SRCDIR) if file.endswith(".h")]
    header_line = "\n".join(['#include "{}"'.format(item) for item in headers])

    ffibuilder.set_source(output_c_extension_name,
                          header_line,
                          sources=sources,
                          extra_compile_args=CFLAGS + INCLUDES,
                          extra_link_args=LIBRARY_DIRS + LINKER_FLAGS,
                          )
    ffibuilder.compile(verbose=True)


def move_output():
    """
    Move the results of the compilation to a directory
    """
    os.makedirs(os.path.join(WORKDIR, EXTENSION_DIR))
    compilation_files = [file for file in os.listdir(WORKDIR) if file.startswith(C_PROJECT_NAME)]
    for file in compilation_files:
        shutil.move(os.path.join(WORKDIR, file), os.path.join(WORKDIR, EXTENSION_DIR, file))


if __name__ == "__main__":
    compile_cffi()
    move_output()
