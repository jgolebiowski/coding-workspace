import argparse
import glob
import os
import pathlib
import shutil
import subprocess

# Working directory
WORKDIR = os.path.dirname(os.path.realpath(__file__))

# directory where CmakeList files are hidden
CMAKE_LISTS_DIR = "cmake-lists"

# Name of the CmakeList for generating a python extension
PYTHON_EXTENSION_CMAKE = "python-extension.cmake"

# Name of the CmakeList for generating a testsuite binary
TEST_EXECUTABLE_CMAKE = "test-executable.cmake"

# Name of the build directory
BUILDDIR = "build"

# CMake project name (also pybinding project name - they must be the same)
PROJECT_NAME_CPP = "example_project_cpp"



def get_config() -> dict:
    parser = argparse.ArgumentParser(
        description="Compile the extension, either as a python extension or as a executable used to run tests")

    helpstring = """
    possible modes (
        test: compile executable runnig the test suite |
        extension: compile a python extension |
        clean: clean the build directory
        )
    """
    parser.add_argument("mode",
                        action="store",
                        type=str,
                        nargs="?",
                        help=helpstring)
    args = parser.parse_args()
    return args.mode


def compile(cmake_filename, binary_suffix=""):
    """
    Compile the module
    """
    source_cmakelist = os.path.join(WORKDIR, CMAKE_LISTS_DIR, cmake_filename)
    target_cmakelist = os.path.join(WORKDIR, "CMakeLists.txt")
    shutil.copyfile(source_cmakelist, target_cmakelist)

    builddir = os.path.join(WORKDIR, BUILDDIR)
    pathlib.Path(builddir).mkdir(parents=True, exist_ok=True)

    os.chdir(builddir)
    cmd = ["cmake", "../"]
    subprocess.run(cmd, check=True)

    cmd = ["make"]
    subprocess.run(cmd, check=True)
    os.chdir(WORKDIR)

    source_binary_prefix = os.path.join(WORKDIR, BUILDDIR, PROJECT_NAME_CPP)
    source_binary = glob.glob(source_binary_prefix + binary_suffix)[0]
    target_binary = os.path.join(WORKDIR, os.path.basename(source_binary))

    if os.path.isfile(target_binary):
        os.remove(target_binary)
    shutil.move(source_binary, target_binary)


def main():
    mode = get_config()

    if mode == "extension":
        compile(PYTHON_EXTENSION_CMAKE, binary_suffix=".cpython*")
    elif mode == "test":
        compile(TEST_EXECUTABLE_CMAKE)
    elif mode == "clean":
        shutil.rmtree(os.path.join(WORKDIR, BUILDDIR))
        os.remove("CMakeLists.txt")
    else:
        print("Must specify a positional argument for mode, see setup.py -h for help")


if __name__ == '__main__':
    main()
