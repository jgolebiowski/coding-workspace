import shutil
from typing import List
from cffi import FFI
import os

WORKDIR = os.path.dirname(os.path.realpath(__file__))
SOURCEDIR = "src"
C_PROJECT_NAME = "_project_extension"
EXTENSION_DIR = os.path.join(WORKDIR, "extension")
C_HEADER = """

///////////////////////////////////////////////////////////////////////////////
// utilities.h
///////////////////////////////////////////////////////////////////////////////
/**
 * @brief Print Hello world
 */
void hello_world();

/**
 * @brief Print hello world with openMP parallelism
 */
void hello_world_omp();

///////////////////////////////////////////////////////////////////////////////
// arraymath.h
///////////////////////////////////////////////////////////////////////////////
/**
 * This function assigns matRES = matA @ matB
 * @param dataA Data for the input matrix
 * @param matArows Dimensions for the input matrix
 * @param matAcols Dimensions for the input matrix
 * @param dataB Data for the input matrix
 * @param matBrows Dimensions for the input matrix
 * @param matBcols Dimensions for the input matrix
 * @param dataRES Data for the output matrix
 * @param matRESrows Dimensions for the output matrix
 * @param matREScols Dimensions for the output matrix
 */
void arraymath_matmul(
        double *dataA, int matArows, int matAcols,
        double *dataB, int matBrows, int matBcols,
        double *dataRES, int matRESrows, int matREScols);
"""


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


def move_output(project_name: str, workdir: str, target_location: str):
    """
    Move the results of the compilation from workdir to the extension location

    :param project_name: Name of the compiled project
    :param workdir: Directory the compilation took place
    :param target_location: location of the extension dir
    """
    os.makedirs(target_location, exist_ok=True)
    compilation_files = [file for file in os.listdir(workdir) if file.startswith(project_name)]
    for file in compilation_files:
        shutil.move(os.path.join(workdir, file), os.path.join(workdir, target_location, file))

    objects = [os.path.join(SOURCEDIR, file) for file in os.listdir(SOURCEDIR) if file.endswith(".o")]
    for object in objects:
        os.remove(object)


if __name__ == "__main__":
    sources = [os.path.join(SOURCEDIR, file) for file in os.listdir(SOURCEDIR) if file.endswith(".cpp")]
    headers = [os.path.join(SOURCEDIR, file) for file in os.listdir(SOURCEDIR) if file.endswith(".h")]
    header_line = "\n".join(['#include "{}"'.format(item) for item in headers])

    compile_cffi(C_PROJECT_NAME, C_HEADER, header_line, sources)
    move_output(C_PROJECT_NAME, WORKDIR, EXTENSION_DIR)
