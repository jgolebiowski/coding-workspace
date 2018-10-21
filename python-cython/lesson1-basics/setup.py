from distutils.core import setup
from distutils.extension import Extension

from Cython.Build import cythonize
import numpy as np

# ------ Package information

NAME = "My cython project"
VERSION = "0.1"
DESCR = "Tamplate for runnig cython"
URL = "https://github.com/jgolebiowski"

AUTHOR = "Jacek Golebiowski"
EMAIL = "golebiowski.j@gmail.com"

LICENSE = "MIT"

# ------ Source directory
SRC_DIR = "supertools/cython"
PACKAGES = [SRC_DIR]

EXTENSIONS = [
    Extension(name="supertools.cython.utilities",
              sources=[
                  SRC_DIR + "/utilities.pyx"
              ],
              libraries=[],
              library_dirs=[],
              include_dirs=[np.get_include()],
              # extra_link_args=['-fopenmp'],
              # extra_compile_args=["-ffast-math", "-fopenmp",
              #                     "-Wall"]
              )
]

if __name__ == "__main__":
    setup(
        name=NAME,
        ext_modules=cythonize(EXTENSIONS),
        packages=PACKAGES,

        version=VERSION,
        description=DESCR,
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        license=LICENSE
    )
