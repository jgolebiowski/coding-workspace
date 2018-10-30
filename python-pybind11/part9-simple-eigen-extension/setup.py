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

# Name of the CmakeList for generating a testsuite executable
TEST_EXECUTABLE_CMAKE = "test-executable.cmake"

# Name of the build directory
BUILDDIR = "build"

# Python project name
PROJECT_NAME = "example_project"

# CMake project name (also pybinding project name - they must be the same)
PROJECT_NAME_CPP = "example_project_cpp"

# Directory where python extension is ot be stored
LIB_DIRECTORY = "clib"


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


def compile_extension():
    """
    Compile the module as an extension
    """
    source_cmakelist = os.path.join(WORKDIR, CMAKE_LISTS_DIR, PYTHON_EXTENSION_CMAKE)
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

    source_library_prefix = os.path.join(WORKDIR, BUILDDIR, PROJECT_NAME_CPP)
    source_library = glob.glob(source_library_prefix + ".cpython*")[0]
    target_location = os.path.join(WORKDIR, PROJECT_NAME, LIB_DIRECTORY, os.path.basename(source_library))

    if os.path.isfile(target_location):
        os.remove(target_location)
    shutil.move(source_library, target_location)


def compile_test():
    """
    Compile the module as an executable to run the test suite
    """
    source_cmakelist = os.path.join(WORKDIR, CMAKE_LISTS_DIR, TEST_EXECUTABLE_CMAKE)
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

    source_executable = os.path.join(WORKDIR, BUILDDIR, PROJECT_NAME_CPP)
    target_executable = os.path.join(WORKDIR, "test_" + PROJECT_NAME_CPP)
    shutil.move(source_executable, target_executable)


def main():
    mode = get_config()

    if mode == "extension":
        compile_extension()
    elif mode == "test":
        compile_test()
    elif mode == "clean":
        shutil.rmtree(os.path.join(WORKDIR, BUILDDIR))
    else:
        print("Must specify a positional argument for mode, see setup.py -h for help")


if __name__ == '__main__':
    main()
